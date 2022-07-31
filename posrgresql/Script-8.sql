

# 1. 생성된 모든 클라이언트 수 - 각 입력란이 채워진 비율
select count(*) from "Client" 

# 2. 생성된 모든 프로젝트 수
select count(*) from "Project"

# 3 생성된 모든 인보이스 수
select count(*) from "Invoice" 

# 4. 인보이스 PDF 다운로드 수 (중복 제거)
select * from "Invoice" 