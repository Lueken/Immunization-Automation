/**************************************************
* Name: WAIIS Immunization Roster
* Group: Enrollment
* Description: Provides the active student roster to WAIIS Immunizations. This excludes students without an SSID and students enrolled in 696
* Notes:
* Date: 1/25/2024
**************************************************/

SELECT DISTINCT
    stu.STATE_STUDENT_NUMBER AS [SSID (Student OSPI#)],
    CASE
        WHEN stu_yr.GRADE = '01' THEN '1'
        WHEN stu_yr.GRADE = '02' THEN '2'
        WHEN stu_yr.GRADE = '03' THEN '3'
        WHEN stu_yr.GRADE = '04' THEN '4'
        WHEN stu_yr.GRADE = '05' THEN '5'
        WHEN stu_yr.GRADE = '06' THEN '6'
        WHEN stu_yr.GRADE = '07' THEN '7'
        WHEN stu_yr.GRADE = '08' THEN '8'
        WHEN stu_yr.GRADE = '09' THEN '9'
        ELSE stu_yr.GRADE
END AS [Grade],
    org.STATE_SCHOOL_CODE AS [School Code (OSPI #)],
    stu.STATE_STUDENT_NUMBER                      AS [SSID (Student OSPI #)],
    COALESCE(per.LEGAL_FN, per.FIRST_NAME)        AS [Student First Name],
    COALESCE(per.LEGAL_MN, per.MIDDLE_NAME)       AS [Student Middle Name],
    COALESCE(per.LEGAL_LN, per.LAST_NAME)         AS [Student Last Name],
    CONVERT(varchar(10), per.BIRTH_DATE, 101) 	AS [DOB],
    per.PRIMARY_PHONE AS [Home Phone Number],
    mail_add.ADDRESS AS [Mailing Address],
    mail_add.CITY AS [City],
    mail_add.STATE AS [State],
    mail_add.ZIP_5 AS [Zip],
    CASE
        WHEN per.GENDER = 'F' THEN 'F'
        WHEN per.GENDER = 'M' THEN 'M'
        WHEN per.GENDER = 'X' THEN 'U'
END  AS [Gender]
FROM EPC_STU_SCH_YR AS stu_yr
    INNER JOIN EPC_STU AS stu ON stu_yr.STUDENT_GU = stu.STUDENT_GU
    LEFT JOIN REV_PERSON AS per ON stu_yr.STUDENT_GU = PER.PERSON_GU
        INNER JOIN REV_ADDRESS AS hm_add ON hm_add.ADDRESS_GU = per.HOME_ADDRESS_GU
        INNER JOIN REV_ADDRESS      AS mail_add ON mail_add.ADDRESS_GU = per.HOME_ADDRESS_GU
    join REV_ORGANIZATION_YEAR  AS org_yr ON stu_yr.ORGANIZATION_YEAR_GU = org_yr.ORGANIZATION_YEAR_GU
         JOIN EPC_SCH AS org ON org_yr.ORGANIZATION_GU = org.ORGANIZATION_GU
        join REV_YEAR AS yr ON org_yr.YEAR_GU = yr.YEAR_GU

WHERE stu_yr.STATUS IS NULL
  AND stu.STATE_STUDENT_NUMBER IS NOT NULL
  AND org.STATE_SCHOOL_CODE != 0
  AND yr.SCHOOL_YEAR = :school_year
  AND yr.EXTENSION = 'R'
order by 1