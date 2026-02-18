# Notion 일자 로그 적재 초안

## 대상
- 페이지: where_my_money 프로젝트 페이지 하위
- 형식: `YYYY-MM-DD 작업 로그`

## 블록 구조
1. 작업 요약
2. 구현/수정 파일
3. 테스트 결과
4. 이슈/리스크
5. 다음 액션

## 최소 필드
- date
- commit_sha
- changed_files
- test_command
- test_result

## 자동화 흐름
1. 작업 완료 후 git 정보 수집
2. `logs/YYYY-MM-DD.md` 파싱
3. Notion API로 블록 append
