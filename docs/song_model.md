# Song Data Model
V1.0 26-07-2026 Initial

-----------------------------------------------------------------------------------------------------------------

| Field             | Type          | Required  | Example            | Notes                                    |
|-------------------|---------------|:---------:|--------------------|------------------------------------------|
| id                | int           | ✅        | 1                 | Unique identifier                         |
| title             | string(300)   | ✅        | Cheerio           | Song title                                |
| artist            | string(300)   | ✅        | Mathie            | Original artist                           |
| duration_seconds  | int           | ✅        | 180               | Stored in seconds                         |
| medley            | bool          | ✅        | false             | Part of a medley                          |
| medley_titles     | string(500)   | ❌        | Song A; Song B    | Only when medley is true                  |
| difficulty        | enum          | ❌        | Medium            | Very Easy, Easy, Medium, Hard, Very Hard  |
| genre             | enum          | ❌        | Pop               | Extendable enum                           |
| tags              | list[string]  | ❌        | Dutch, Party, Tent| Multiple tags allowed                     |
| release_year      | int           | ✅        | 2020              | 1980, 1990, 2000, 2010, 2020              |
| lead_vocals       | list[string]  | ❌        | Bianca            | Main vocalist(s)                          |
| is_core_repertoire| bool          | ❌        | true              | Frequently played                         |
| party_score       | int           | ❌        | 10                | Score 1–10                                |
| original_key      | string(2)     | ❌        | E                 | Original key                              |
| transpose_to      | string(2)     | ❌        | F                 | Performance key                           |
| created_at        | date          | ✅        | 2026-07-26        | Creation date                             |
| updated_at        | date          | ❌        | 2026-08-01        | Last modification                         |
| notes             | string(500)   | ❌        | 1 x refrein ...   | open text area                            |

-----------------------------------------------------------------------------------------------------------------