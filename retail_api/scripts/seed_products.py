"""
商品种子数据脚本。在项目根目录执行：
  PYTHONPATH=. python -m retail_api.scripts.seed_products
"""
import uuid

from retail_api.db.base import Base
from retail_api.db.session import engine, SessionLocal
from retail_api.product.models import Product


PRODUCTS = [
    ("北欧风陶瓷马克杯", "nordic-ceramic-mug", "优质陶瓷，手感温润，多色可选。微波炉与洗碗机适用。", 49.0, 120),
    ("无线蓝牙耳机", "wireless-bluetooth-earphones", "主动降噪，续航 24 小时，舒适佩戴。", 299.0, 80),
    ("便携咖啡手冲壶", "portable-pour-over-kettle", "304 不锈钢，细长壶嘴，精准控流。", 159.0, 45),
    ("竹纤维毛巾三件套", "bamboo-towel-set", "柔软吸水，抑菌透气，灰/白/米三色。", 89.0, 200),
    ("香薰加湿器", "aromatherapy-humidifier", "静音喷雾，LED 夜灯，可加精油。", 129.0, 60),
    ("懒人沙发豆袋", "bean-bag-sofa", "内填 EP 粒子，可拆洗外套，多色。", 199.0, 35),
    ("不锈钢保温杯 500ml", "stainless-steel-tumbler-500", "保冷保热 12 小时，一键开盖。", 79.0, 150),
    ("桌面收纳盒组合", "desk-organizer-set", "磨砂质感，多格分区，可叠放。", 59.0, 90),
    ("护眼台灯", "eye-care-lamp", "无频闪，多档调光调色温，触控。", 169.0, 55),
    ("瑜伽垫 6mm", "yoga-mat-6mm", "NBR 材质，防滑纹路，附收纳带。", 69.0, 100),
    ("玻璃冷水壶 1.2L", "glass-water-pitcher-1-2l", "高硼硅玻璃，带刻度，可冷藏。", 45.0, 130),
    ("软木记事板", "cork-board", "A3 尺寸，配图钉，可挂墙。", 39.0, 75),
    ("便携榨汁杯", "portable-blender-cup", "USB 充电，一键搅拌，随行杯设计。", 99.0, 70),
    ("羊毛混纺围巾", "wool-blend-scarf", "秋冬款，柔软不扎，多色。", 129.0, 40),
    ("硅胶保鲜盖套装", "silicone-lid-set", "多种尺寸，密封防漏，可重复使用。", 35.0, 180),
    ("迷你投影仪", "mini-projector", "1080P，便携投屏，内置电池。", 599.0, 25),
    ("手账本 A5", "journal-a5", "内页点阵/方格/空白可选，精装。", 45.0, 110),
    ("电动牙刷", "electric-toothbrush", "声波震动，2 分钟定时，多档位。", 189.0, 65),
    ("挂耳咖啡 10 包", "pour-over-coffee-10", "埃塞俄比亚耶加雪菲，中浅焙。", 58.0, 200),
    ("毛绒靠垫", "plush-cushion", "天鹅绒面料，多色，45x45cm。", 79.0, 85),
    ("桌面绿植盆栽", "desk-plant-pot", "含盆含土，易养护品种，净化空气。", 49.0, 60),
    ("手机支架", "phone-stand", "铝合金，多角度调节，折叠便携。", 29.0, 250),
    ("蒸汽眼罩 5 片装", "steam-eye-mask-5", "无香料，约 40°C 温热，助眠。", 35.0, 140),
    ("帆布托特包", "canvas-tote", "大容量，内袋，米白/藏青。", 89.0, 55),
    ("智能体脂秤", "smart-scale", "APP 连接，多项身体数据。", 149.0, 45),
    ("磨砂玻璃杯 对装", "frosted-glass-cup-pair", "350ml，可微波，简约款。", 55.0, 95),
    ("扩香石套装", "diffuser-stone-set", "天然石材 + 精油 10ml，多味可选。", 68.0, 70),
    ("便携餐具三件套", "portable-cutlery-set", "不锈钢 + 收纳盒，环保可重复。", 42.0, 120),
    ("懒人叠叠乐", "stacking-tray", "可叠放收纳，北欧风，多色。", 65.0, 80),
    ("香氛蜡烛", "scented-candle", "大豆蜡，约 30h 燃烧，木质香调。", 59.0, 90),
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Product).count()
        if existing > 0:
            print(f"已有 {existing} 件商品，跳过种子（如需重灌请先清空 products 表）")
            return
        for name, slug, description, price, stock in PRODUCTS:
            p = Product(
                id=uuid.uuid4().hex,
                name=name,
                slug=slug,
                description=description,
                price=price,
                stock=stock,
            )
            db.add(p)
        db.commit()
        print(f"已写入 {len(PRODUCTS)} 件商品")
    finally:
        db.close()


if __name__ == "__main__":
    main()
