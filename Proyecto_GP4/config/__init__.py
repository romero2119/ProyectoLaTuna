import pymysql

pymysql.version_info = (2, 2, 8, "final", 0)  # Esto engaña a Django haciéndole creer que es mysqlclient
pymysql.install_as_MySQLdb()