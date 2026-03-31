#!/bin/bash
# 宝宸管理系统 MVP 验证脚本
# 用法: bash tests/mvp_test.sh

BASE="http://localhost:8000"
FRONT="http://localhost:3000"
PASS=0; FAIL=0; ERRORS=""

check() {
  local name="$1" result="$2"
  if echo "$result" | grep -q '"detail"'; then
    echo "❌ $name"; echo "   → $(echo "$result" | head -1)"; FAIL=$((FAIL+1)); ERRORS="$ERRORS\n  ❌ $name"
  else
    echo "✅ $name"; PASS=$((PASS+1))
  fi
}

echo "========================================="
echo "  宝宸管理系统 MVP 验证"
echo "========================================="

# 1. 连通性
echo -e "\n📡 1. 连通性\n-----------------------------------------"
R=$(curl -s "$BASE/health"); check "后端健康检查" "$R"
R=$(curl -s -o /dev/null -w "%{http_code}" "$FRONT")
[ "$R" = "200" ] && { echo "✅ 前端页面 (HTTP $R)"; PASS=$((PASS+1)); } || { echo "❌ 前端页面 (HTTP $R)"; FAIL=$((FAIL+1)); }

# 2. 认证
echo -e "\n🔐 2. 认证系统\n-----------------------------------------"
R=$(curl -s -X POST "$BASE/api/v1/auth/login" -H "Content-Type: application/json" -d '{"email":"admin@baochen.com","password":"admin123"}')
TOKEN=$(echo "$R" | python3 -c "import sys,json;print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")
if [ -n "$TOKEN" ]; then echo "✅ 登录成功"; PASS=$((PASS+1)); else echo "❌ 登录失败: $R"; exit 1; fi
AUTH="Authorization: Bearer $TOKEN"
R=$(curl -s "$BASE/api/v1/auth/me" -H "$AUTH"); check "获取当前用户" "$R"

# 3. 客户CRUD
echo -e "\n👥 3. 客户管理\n-----------------------------------------"
R=$(curl -s "$BASE/api/v1/clients/" -H "$AUTH"); check "客户列表" "$R"
R=$(curl -s -X POST "$BASE/api/v1/clients/" -H "$AUTH" -H "Content-Type: application/json" -d '{"name":"MVP测试公司","contact_person":"王五","phone":"13900139000"}')
CID=$(echo "$R" | python3 -c "import sys,json;d=json.load(sys.stdin).get('data',json.load(sys.stdin));print(d.get('id',''))" 2>/dev/null || echo "")
check "创建客户(ID=$CID)" "$R"
[ -n "$CID" ] && { R=$(curl -s -X PUT "$BASE/api/v1/clients/$CID" -H "$AUTH" -H "Content-Type: application/json" -d '{"name":"MVP测试公司-改","contact_person":"王五","phone":"13900139000"}'); check "更新客户" "$R"; }

# 4. 案件CRUD
echo -e "\n📋 4. 案件管理\n-----------------------------------------"
R=$(curl -s "$BASE/api/v1/cases/" -H "$AUTH"); check "案件列表" "$R"
if [ -n "$CID" ]; then
  R=$(curl -s -X POST "$BASE/api/v1/cases/" -H "$AUTH" -H "Content-Type: application/json" \
    -d "{\"title\":\"MVP测试发明\",\"client_id\":$CID,\"patent_type\":\"发明\",\"applicant\":\"测试\",\"inventor\":\"赵六\"}")
  CSID=$(echo "$R" | python3 -c "import sys,json;d=json.load(sys.stdin).get('data',json.load(sys.stdin));print(d.get('id',''))" 2>/dev/null || echo "")
  CNUM=$(echo "$R" | python3 -c "import sys,json;d=json.load(sys.stdin).get('data',json.load(sys.stdin));print(d.get('case_number',''))" 2>/dev/null || echo "")
  check "创建案件(ID=$CSID 编号=$CNUM)" "$R"
fi
[ -n "$CSID" ] && { R=$(curl -s "$BASE/api/v1/cases/$CSID" -H "$AUTH"); check "获取案件详情" "$R"; }
[ -n "$CSID" ] && { R=$(curl -s -X PUT "$BASE/api/v1/cases/$CSID" -H "$AUTH" -H "Content-Type: application/json" -d '{"title":"MVP测试发明-改","patent_type":"发明"}'); check "更新案件" "$R"; }
[ -n "$CSID" ] && { R=$(curl -s -X PATCH "$BASE/api/v1/cases/$CSID/status" -H "$AUTH" -H "Content-Type: application/json" -d '{"status":"撰写中"}'); check "更新案件状态" "$R"; }

# 5. 搜索和统计
echo -e "\n🔍 5. 搜索与统计\n-----------------------------------------"
R=$(curl -s "$BASE/api/v1/cases/search?keyword=MVP" -H "$AUTH"); check "案件搜索" "$R"
R=$(curl -s "$BASE/api/v1/cases/statistics" -H "$AUTH"); check "案件统计" "$R"

# 6. 前端API代理
echo -e "\n🌐 6. 前端→后端代理\n-----------------------------------------"
R=$(curl -s "$FRONT/api/v1/cases/" -H "$AUTH")
check "前端代理案件列表" "$R"

# 结果
echo -e "\n========================================="
echo "  结果: ✅ $PASS 通过  ❌ $FAIL 失败"
if [ $FAIL -gt 0 ]; then echo -e "失败项:$ERRORS"; fi
echo "========================================="
[ $FAIL -eq 0 ] && echo "🎉 MVP 验证通过！" || echo "⚠️ 存在问题，需要修复"
