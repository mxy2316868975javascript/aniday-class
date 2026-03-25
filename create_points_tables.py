from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://ddclass:iTiipYXa64BjM7bF@81.70.103.192:5432/ddclass"

def create_points_tables():
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        trans = conn.begin()

        try:
            # 1. 创建 point_rules 表
            print("创建 point_rules 表...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS point_rules (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL UNIQUE,
                    description VARCHAR,
                    category VARCHAR NOT NULL,
                    points INTEGER NOT NULL,
                    condition_type VARCHAR NOT NULL,
                    condition_value VARCHAR,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """))
            print("✅ point_rules 表创建成功")

            # 2. 创建 student_points 表
            print("创建 student_points 表...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS student_points (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL UNIQUE REFERENCES students(id) ON DELETE CASCADE,
                    total_points INTEGER DEFAULT 0,
                    available_points INTEGER DEFAULT 0,
                    total_earned INTEGER DEFAULT 0,
                    total_spent INTEGER DEFAULT 0,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """))
            print("✅ student_points 表创建成功")

            # 3. 创建 point_records 表
            print("创建 point_records 表...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS point_records (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                    rule_id INTEGER REFERENCES point_rules(id),
                    points INTEGER NOT NULL,
                    balance_after INTEGER NOT NULL,
                    source_type VARCHAR NOT NULL,
                    source_id INTEGER,
                    description VARCHAR,
                    operator_id INTEGER REFERENCES users(id),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """))
            print("✅ point_records 表创建成功")

            # 4. 创建 point_items 表
            print("创建 point_items 表...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS point_items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    description VARCHAR,
                    item_type VARCHAR NOT NULL,
                    points_cost INTEGER NOT NULL,
                    stock INTEGER DEFAULT -1,
                    image_url VARCHAR,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """))
            print("✅ point_items 表创建成功")

            # 5. 创建 point_exchanges 表
            print("创建 point_exchanges 表...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS point_exchanges (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                    item_id INTEGER NOT NULL REFERENCES point_items(id),
                    points_spent INTEGER NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    status VARCHAR DEFAULT 'pending',
                    exchange_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    pickup_time TIMESTAMP WITH TIME ZONE,
                    operator_id INTEGER REFERENCES users(id),
                    remark VARCHAR
                )
            """))
            print("✅ point_exchanges 表创建成功")

            # 创建索引
            print("\n创建索引...")
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_point_records_student_id ON point_records(student_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_point_records_created_at ON point_records(created_at DESC)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_point_exchanges_student_id ON point_exchanges(student_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_point_exchanges_status ON point_exchanges(status)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_student_points_student_id ON student_points(student_id)"))
            print("✅ 索引创建成功")

            # 插入默认积分规则
            print("\n插入默认积分规则...")
            default_rules = [
                ("全勤奖励", "每月全勤奖励", "attendance", 50, "attendance_full_month", None),
                ("考勤优秀", "一周内无迟到早退", "attendance", 20, "attendance_weekly", None),
                ("成绩优秀", "单科90分以上", "score", 30, "score_excellent", "90"),
                ("成绩进步", "相比上次进步10分以上", "score", 25, "score_improve", "10"),
                ("班级贡献", "帮助同学或老师", "behavior", 10, "behavior_contribution", None),
                ("遵守纪律", "一周内无违纪记录", "behavior", 15, "behavior_discipline", None),
                ("卫生优秀", "班级卫生检查优秀", "behavior", 10, "behavior_sanitation", None),
                ("积极发言", "课堂上积极发言", "behavior", 5, "behavior_participation", None),
                ("作业优秀", "作业被评优", "homework", 10, "homework_excellent", None),
                ("竞赛获奖", "校级竞赛获奖", "competition", 50, "competition_school", None),
            ]

            for name, desc, category, points, cond_type, cond_val in default_rules:
                conn.execute(text("""
                    INSERT INTO point_rules (name, description, category, points, condition_type, condition_value, is_active)
                    VALUES (:name, :desc, :category, :points, :cond_type, :cond_val, TRUE)
                    ON CONFLICT (name) DO NOTHING
                """), {"name": name, "desc": desc, "category": category, "points": points, "cond_type": cond_type, "cond_val": cond_val})

            print("✅ 默认积分规则插入成功")

            # 插入默认商品
            print("\n插入默认商品...")
            default_items = [
                ("学习之星徽章", "荣誉象征，永久佩戴", "virtual", 100, -1),
                ("班级管理员", "获得班级管理权限一天", "virtual", 150, -1),
                ("免作业卡", "可免做一次作业", "virtual", 80, 10),
                ("优先选座权", "可优先选择座位一天", "virtual", 50, -1),
                ("文具套装", "一套精美文具", "physical", 200, 5),
                ("课外书籍", "一本适合年龄的课外书", "physical", 300, 3),
                ("电影票", "一张电影票", "physical", 500, 2),
            ]

            for name, desc, item_type, cost, stock in default_items:
                conn.execute(text("""
                    INSERT INTO point_items (name, description, item_type, points_cost, stock, is_active)
                    VALUES (:name, :desc, :item_type, :cost, :stock, TRUE)
                    ON CONFLICT DO NOTHING
                """), {"name": name, "desc": desc, "item_type": item_type, "cost": cost, "stock": stock})

            print("✅ 默认商品插入成功")

            # 为所有学生创建积分账户
            print("\n为所有学生创建积分账户...")
            conn.execute(text("""
                INSERT INTO student_points (student_id, total_points, available_points, total_earned, total_spent)
                SELECT id, 0, 0, 0, 0 FROM students
                WHERE NOT EXISTS (SELECT 1 FROM student_points WHERE student_points.student_id = students.id)
            """))
            print("✅ 学生积分账户创建成功")

            trans.commit()
            print("\n" + "="*50)
            print("🎉 积分系统数据库创建完成！")
            print("="*50)

        except Exception as e:
            trans.rollback()
            print(f"\n❌ 创建失败: {e}")
            raise

if __name__ == "__main__":
    create_points_tables()
