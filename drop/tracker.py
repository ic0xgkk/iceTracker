import psutil
import time
import sqlite3


def init_db(conn):
    cursor = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS global(
    sys_time FLOAT UNSIGNED NOT NULL,
    cpu_user FLOAT UNSIGNED,
    cpu_system FLOAT UNSIGNED,
    cpu_idle FLOAT UNSIGNED,
    cpu_iowait FLOAT UNSIGNED,
    cpu_load_1 FLOAT UNSIGNED,
    cpu_load_5 FLOAT UNSIGNED,
    cpu_load_15 FLOAT UNSIGNED,
	phymem_total BIGINT UNSIGNED,
	phymem_available BIGINT UNSIGNED,
	phymem_used BIGINT UNSIGNED,
	phymem_buffers BIGINT UNSIGNED,
	phymem_cached BIGINT UNSIGNED,
	phymem_shared BIGINT UNSIGNED,
	phymem_free BIGINT UNSIGNED,
	swmem_total BIGINT UNSIGNED,
	swmem_used BIGINT UNSIGNED,
	swmem_free BIGINT UNSIGNED
)"""
    cursor.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS process(
    sys_time FLOAT UNSIGNED NOT NULL,
	pid INT UNSIGNED,
	name TEXT,
	exe TEXT,
	cmdline TEXT,
	create_time FLOAT,
	parent INT,
	user TEXT,
	threads INT,
	cpu_user FLOAT UNSIGNED,
	cpu_sys FLOAT UNSIGNED,
	cpu_iowait FLOAT UNSIGNED,
	phymem_used BIGINT UNSIGNED,
	mtlmem_used BIGINT UNSIGNED,
	swmem_used BIGINT UNSIGNED,
	mem_lib_used BIGINT UNSIGNED,
	mem_map LONGTEXT
)"""
    cursor.execute(sql)
    conn.commit()
    cursor.close()

