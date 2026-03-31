"""
编号生成器服务
案件编号格式：BCZL + 年月(6位) + 类型(1位: 1发明/2实用新型/3外观) + 流水号(3位)
示例：BCZL2026031001
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case


class NumberingService:
    """编号生成服务"""

    # 专利类型到类型码的映射
    PATENT_TYPE_CODES = {
        "发明": "1",
        "发明专利": "1",
        "实用新型": "2",
        "实用新型专利": "2",
        "外观设计": "3",
        "外观": "3",
        "外观专利": "3",
    }

    @classmethod
    def get_type_code(cls, patent_type: str) -> str:
        """
        获取专利类型对应的类型码

        Args:
            patent_type: 专利类型（发明/实用新型/外观设计等）

        Returns:
            类型码（1/2/3），未知类型返回 '0'
        """
        return cls.PATENT_TYPE_CODES.get(patent_type, "0")

    @classmethod
    async def generate_case_number(
        cls,
        db: AsyncSession,
        patent_type: str,
        prefix: str = "BCZL"
    ) -> str:
        """
        生成案件编号

        格式：前缀 + 年月(6位) + 类型码(1位) + 流水号(3位)
        示例：BCZL2026031001

        Args:
            db: 数据库会话
            patent_type: 专利类型
            prefix: 编号前缀，默认 BCZL

        Returns:
            生成的案件编号
        """
        # 获取当前年月
        now = datetime.now()
        year_month = now.strftime("%Y%m")

        # 获取类型码
        type_code = cls.get_type_code(patent_type)

        # 构建编号前缀模式（用于查询当月该类型的最大编号）
        # 例如：BCZL2026031%
        number_prefix = f"{prefix}{year_month}{type_code}"

        # 查询当月该类型的最大编号
        stmt = select(func.max(Case.case_number)).where(
            Case.case_number.like(f"{number_prefix}%")
        )
        result = await db.execute(stmt)
        max_number = result.scalar_one_or_none()

        # 计算下一个流水号
        if max_number:
            # 从最大编号中提取流水号并+1
            try:
                last_sequence = int(max_number[-3:])
                next_sequence = last_sequence + 1
            except (ValueError, IndexError):
                next_sequence = 1
        else:
            next_sequence = 1

        # 格式化流水号为3位（左侧补零）
        sequence_str = f"{next_sequence:03d}"

        # 生成完整编号
        case_number = f"{number_prefix}{sequence_str}"

        return case_number

    @classmethod
    async def generate_case_number_with_retry(
        cls,
        db: AsyncSession,
        patent_type: str,
        prefix: str = "BCZL",
        max_retries: int = 3
    ) -> str:
        """
        生成案件编号（带重试机制，防止并发冲突）

        Args:
            db: 数据库会话
            patent_type: 专利类型
            prefix: 编号前缀
            max_retries: 最大重试次数

        Returns:
            生成的案件编号

        Raises:
            RuntimeError: 重试次数耗尽仍无法生成唯一编号
        """
        for attempt in range(max_retries):
            case_number = await cls.generate_case_number(db, patent_type, prefix)

            # 检查编号是否已存在
            stmt = select(Case).where(Case.case_number == case_number)
            result = await db.execute(stmt)
            existing_case = result.scalar_one_or_none()

            if not existing_case:
                return case_number

        raise RuntimeError(f"无法生成唯一的案件编号，已重试 {max_retries} 次")
