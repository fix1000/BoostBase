# Song Data Model
V1.0 26-07-2026 Initial
V1.1 15-09-2026 Added Validations

-----------------------------------------------------------------------------------------------------------------

| Field             | Type          | Required  | Example            | Notes                                    | Validations
|-------------------|---------------|:---------:|--------------------|------------------------------------------|--------------
| id                | int           | ✅        | 1                 | Unique identifier                         | Must be int and > 0
| title             | string(300)   | ✅        | Cheerio           | Song title                                | Cannot be None or empty. 
| artist            | string(300)   | ✅        | Mathie            | Original artist                           | Cannot be None or empty. 
| duration_seconds  | int           | ✅        | 180               | Stored in seconds                         | Must be int and is between 10 - 1000
| medley            | bool          | ✅        | false             | Part of a medley                          | Must be True or False
| medley_titles     | list[string]  | ❌        | Song A; Song B    | Only when medley is true                  | Must be a list of strings, mandatory filled when medley = True.
| difficulty        | enum          | ❌        | Medium            | Very Easy, Easy, Medium, Hard, Very Hard  | One of Very Easy, Easy, Medium, Hard, Very Hard
| genre             | enum          | ❌        | Pop               | Extendable enum                           | Enum
| tags              | list[string]  | ❌        | Dutch, Party, Tent| Multiple tags allowed                     | Must be a list of strings
| release_year      | int           | ✅        | 2020              | 1980, 1990, 2000, 2010, 2020              | Must be int between 1900 en 2100
| lead_vocals       | list[string]  | ❌        | ["Gilbert"]       | Main vocalist(s)                          | Must be a list of strings
| is_core_repertoire| bool          | ❌        | true              | Frequently played                         | Must be true or false
| party_score       | int           | ❌        | 10                | Score 1–10                                | Must be None or int between 1-10
| original_key      | string(2)     | ❌        | E                 | Original key                              | Must be None or filled with 1 or 2 characters
| transpose_to      | string(2)     | ❌        | F                 | Performance key                           | Must be None or filled with 1 or 2 characters
| created_at        | datetime      | ✅        | 2026-07-26        | Creation date                             | Must be a datetime, between year 2026 and higher
| updated_at        | datetime      | ❌        | 2026-08-01        | Last modification                         | Must be a datetime, between year 2026 and higher
| notes             | string(500)   | ❌        | 1 x refrein ...   | open text area                            | None

-----------------------------------------------------------------------------------------------------------------