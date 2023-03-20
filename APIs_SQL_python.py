import time

import numpy as np
from sqlalchemy import (Table, Column, BigInteger, Integer, Text, MetaData, create_engine, DateTime, Index)
import requests
import warnings

warnings.filterwarnings("ignore")


def driver():
    """

    :return: runs the code
    """
    con_string = "mysql+pymysql://root:123456789@127.0.0.1:3306"

    git_token = "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"
    # Will expire by 15 March

    headers = {'Authorization': 'token ' + git_token}

    repo_url = "https://api.github.com/repos/apache/hadoop/contributors?per_page=100"

    features = ["login", "id", "location", "email", "hireable", "bio", "twitter_username", "public_repos",
                "public_gists", "followers", "following", "created_at"]

    r = requests.get(repo_url, headers=headers)
    time.sleep(10)

    apache_hadoop_contributors = r.json()

    def get_user_api(dict_user, imp_features):
        """
        :param dict_user: Contributor dictionary
        :param imp_features: list of features needed from each users
        :return: returns a dictionary
        """
        user_url = dict_user['url']
        user_request = requests.get(user_url, headers=headers)
        time.sleep(5)
        user_details = user_request.json()
        try:
            user_useful_info = {k: v for k, v in user_details.items() if k in imp_features}
            user_useful_info['created_at'] = np.datetime64(user_useful_info['created_at'])
        except:
            user_useful_info = {}
            print(user_details)
        return user_useful_info

    all_user_details = []

    for _ in apache_hadoop_contributors:
        this_one_user = get_user_api(_, features)
        print(this_one_user)
        all_user_details.append(this_one_user)

    engine = create_engine(con_string, echo=False)
    conn = engine.connect()

    data_base_query = """CREATE DATABASE IF NOT EXISTS ddr_homework;"""

    conn.execute(data_base_query);
    time.sleep(2)
    drop_table_query = """DROP TABLE IF EXISTS ddr_homework.git_users_apache_hadoop;"""

    conn.execute(drop_table_query);
    time.sleep(2)

    meta_data = MetaData(schema='ddr_homework')

    git_user_table = Table('git_users_apache_hadoop', meta_data,
                           Column('login', Text(100)),
                           Column('id', BigInteger, primary_key=True),
                           Column('location', Text(150)),
                           Column('email', Text(100)),
                           Column('hireable', Text(20)),
                           Column('bio', Text(20)),
                           Column('twitter_username', Text(20)),
                           Column('public_repos', Integer),
                           Column('public_gists', Integer),
                           Column('followers', Integer),
                           Column('following', Integer),
                           Column('created_at', DateTime)
                           )
    Index('idx_login', git_user_table.c.login, mysql_length=150)
    Index('idx_location', git_user_table.c.location, mysql_length=150)
    Index('idx_hireable', git_user_table.c.hireable, mysql_length=150)

    try:
        meta_data.create_all(conn)
    except:
        print("Table exists :)")

    insert_command = git_user_table.insert().values(all_user_details)

    print(insert_command)

    conn.execute(insert_command)


if __name__ == "__main__":
    driver()
