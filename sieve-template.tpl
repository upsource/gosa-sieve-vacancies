# generate and autoupdated by sync-vacancies.py
#
#

require ["vacation","date","relational","variables"];

if header :matches "Subject" "*" {
    set "subjwas" ": ${1}";
}

if allof(currentdate :value "ge" "date" "{gosaVacationStartDate}",
         currentdate :value "le" "date" "{gosaVacationStopDate}"){{
  # Reply at most once a day to a same sender
  vacation
  :days 1
  :subject "Abwesenheitsnotiz Re:"{subjwas}
  "{gosaVacationMessage}";

}}