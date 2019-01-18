# generate and autoupdated by sync-vacancies.py
#
#

require ["vacation","date","relational","variables"];

# rule:[autogen by gosa-sieve-vacancies.deb]
if header :matches "Subject" "*" {{
    set "subjwas" "${{1}}";
}}

# rule:[autogen by gosa-sieve-vacancies.deb]
if allof(currentdate :value "ge" "date" "{gosaVacationStartDate}",
            currentdate :value "le" "date" "{gosaVacationStopDate}",
            not header :is "X-Spam" "Yes",
            not header :contains "X-Spam-Flag" "YES"){{
    # Reply at most once a day to a same sender
    vacation
        :days 1
        :subject "Abwesenheitsnotiz Re: ${{subjwas}}"
        "{gosaVacationMessage}";

}}
