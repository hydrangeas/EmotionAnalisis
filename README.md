# EmotionAnalisis

## How to use

1. Make setup.yml

like this..

    DB:
      host    : database.abcdefgh123a.us-west-2.rds.amazonaws.com
      user    : user
      pass    : pass
      charset : utf8
      dbname  : table
    
    TWITTER:
      access_token  : 1234567890-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLM
      access_secret : a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w
      api_key       : ABCDEFGHIJKLMNOPQRSTUVWXY
      api_secret    : 1A2B3C4D56E7F8G9H0I1J2K3L4M5N6O7P8Q9R0S1T2U3V4W5X6

2. Execute `db_setup.py`
BEFORE check your mysql server settings. MUST `character_set_client` `character_set_connection` `character_set_database` `character_set_filesystem` `character_set_result` `character_set_server` `character_set_system` is `UTF-8`.

3. Make config.yml

like this..

    ---
    DICT:
      tono: ["殿", "殿、利息でござる！"]

4. Execute `register_dict.py`
5. Execute `get_tweet.py`



