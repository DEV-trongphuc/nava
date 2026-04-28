import json
import re

json_data = """{
  "error": 0,
  "error_msg": "success",
  "data": {
    "items": [
      {
        "userid": 62142497,
        "author_username": "vanthangmtd",
        "author_portrait": "",
        "product_items": [
          {
            "name": "Đế dựng đa năng cho máy tính Mini PC, điều chỉnh được, nhỏ gọn, tinh tế cho bàn làm việc",
            "image": "vn-11134207-820l4-mir6bh17pj4426",
            "model_name": "⑴  Đế Dựng Nhỏ"
          }
        ],
        "ItemRatingReply": null
      },
      {
        "author_username": "vanthangmtd",
        "author_portrait": "",
        "product_items": [
          {
            "name": "Workstation Server Minisforum MS01 SFP+ 10Gbps MS-01 băng thông 10GB Máy trạm / chủ",
            "image": "vn-11134207-820l4-metdd3xjbwg2d8",
            "model_name": "i5 12600H 4.5Ghz 16T,NO RAM - NO SSD"
          }
        ],
        "ItemRatingReply": null
      },
      {
        "author_username": "vutuannn",
        "author_portrait": "vn-11134233-7ras8-m4enw6q4rdu792",
        "product_items": [
          {
            "name": "RAM Laptop 16GB DDR5 5600 MHz - Samsung, Crucial, SK Hynix, Micron - Ram Mini PC Nhập Khẩu BH 3 Năm",
            "image": "vn-11134207-81ztc-mn2d789xy1ae0a",
            "model_name": "CRUCIAL,16GB Single"
          }
        ],
        "ItemRatingReply": {
          "comment": "Cảm ơn Quý khách  vutuannn  đã tin tưởng và ủng hộ NavaStore. Shop hy vọng sản phẩm sẽ đem lại nhiều cảm hứng và hiệu quả cho công việc của Quý khách ạ! ☺️"
        }
      },
      {
        "author_username": "ukshop12345",
        "author_portrait": "c95ab40a615612b04ff68211d7c30fb8",
        "product_items": [
          {
            "name": "SSD Predator GM7000 1TB 2TB 4TB NVMe Gen 4 PCIe Có DRAM Tốc độ Cao, Có HeadSink tích hợp, BH 5 năm",
            "image": "vn-11134207-81ztc-mmtu6wrm7kzkb4",
            "model_name": "New FullBox - 2TB"
          }
        ],
        "ItemRatingReply": {
          "comment": "Cảm ơn Quý khách  ukshop12345  đã tin tưởng và ủng hộ NavaStore. Shop hy vọng sản phẩm sẽ đem lại nhiều cảm hứng và hiệu quả cho công việc của Quý khách ạ! ☺️"
        }
      },
      {
        "author_username": "ukshop12345",
        "author_portrait": "c95ab40a615612b04ff68211d7c30fb8",
        "product_items": [
          {
            "name": "Ốc vít ổ cứng SSD M2, Card Wifi thép không gỉ, cho Máy tính Laptop PC Main fan Linh kiện | M2 M2x3",
            "image": "vn-11134207-820l4-mjrrj44pvy80d2",
            "model_name": "Ốc SSD M2 (1 con)"
          }
        ],
        "ItemRatingReply": {
          "comment": "Cảm ơn Quý khách  ukshop12345  đã tin tưởng và lựa chọn mua hàng tại NavaStore. Nếu có vấn đề gì chưa hài lòng hãy nhắn lại ngay cho shop để được hỗ trợ và xử lí nhanh nhất ạ. Shop luôn hy vọng được tiếp tục đồng hành cùng Quý khách trong tương lai ạ. ☺️"
        }
      },
      {
        "author_username": "lnphm994",
        "author_portrait": "",
        "product_items": [
          {
            "name": "Đế dựng đa năng cho máy tính Mini PC, điều chỉnh được, nhỏ gọn, tinh tế cho bàn làm việc",
            "image": "vn-11134207-820l4-mir6bh17pj4426",
            "model_name": "⑵ Đế Dựng Lớn"
          }
        ],
        "ItemRatingReply": {
          "comment": "Cảm ơn Quý khách  lnphm994  đã tin tưởng và lựa chọn mua hàng tại NavaStore. Nếu có vấn đề gì chưa hài lòng hãy nhắn lại ngay cho shop để được hỗ trợ và xử lí nhanh nhất ạ. Shop luôn hy vọng được tiếp tục đồng hành cùng Quý khách trong tương lai ạ. ☺️"
        }
      }
    ]
  }
}"""

data = json.loads(json_data)

html_cards = []
for item in data['data']['items']:
    username = item['author_username']
    portrait = item['author_portrait']
    if portrait:
        avatar_html = f'<img src="https://cf.shopee.vn/file/{portrait}_tn" alt="{username}">'
    else:
        avatar_html = f'{username[0].upper()}'
    
    product = item['product_items'][0]
    p_name = product['name']
    p_img = product['image']
    p_model = product['model_name']
    
    reply = item.get('ItemRatingReply')
    
    if reply and reply.get('comment'):
        reply_html = f'''
                    <div class="sc-reply">
                        <strong>Phản hồi của Người bán:</strong>
                        <p>{reply['comment']}</p>
                    </div>'''
    else:
        reply_html = ''

    card = f'''                <div class="shopee-comment-card">
                    <div class="sc-header">
                        <div class="sc-avatar">{avatar_html}</div>
                        <div class="sc-meta">
                            <h4>{username}</h4>
                            <div class="sc-stars">
                                <i class="ph-fill ph-star"></i><i class="ph-fill ph-star"></i><i class="ph-fill ph-star"></i><i class="ph-fill ph-star"></i><i class="ph-fill ph-star"></i>
                            </div>
                        </div>
                    </div>
                    <div class="sc-body">
                        <div class="sc-default">Chất lượng sản phẩm tuyệt vời, đóng gói rất đẹp và chắc chắn!</div>
                        <div class="sc-product">
                            <img src="https://cf.shopee.vn/file/{p_img}" alt="Product">
                            <div class="sc-p-info">
                                <span class="sc-p-name">{p_name}</span>
                                <span class="sc-p-model">Phân loại: {p_model}</span>
                            </div>
                        </div>
                    </div>{reply_html}
                </div>'''
    html_cards.append(card)

grid_content = '\n'.join(html_cards)

new_section = f'''
        <!-- Shopee Reviews Section -->
        <section class="shopee-reviews-section">
            <div class="container">
                <div class="section-header testi-section-header-v2">
                    <div class="testi-badge" style="background: rgba(238, 77, 45, 0.1); border-color: rgba(238, 77, 45, 0.2); color: #ee4d2d;"><i class="ph-fill ph-shopping-cart"></i> Đánh giá trên Shopee</div>
                    <h2 class="section-title">Nhận Xét Từ Gian Hàng <span>Shopee</span></h2>
                </div>
                <div class="shopee-comments-grid">
{grid_content}
                </div>
            </div>
        </section>
'''

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Append below the testimonial section
# Let's find the end of testimonial-section
pattern = re.compile(r'(</section>\s*<!-- FAQ Section -->)')
new_content = pattern.sub(new_section + r'\1', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)


# CSS addition
css = """
/* --- SHOPEE REVIEWS SECTION --- */
.shopee-reviews-section {
    padding: 60px 0;
    background: var(--bg-gray);
}
.shopee-comments-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 20px;
}
.shopee-comment-card {
    background: var(--bg-white);
    border-radius: var(--radius-md);
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    border: 1px solid var(--border-color);
}
.sc-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
}
.sc-avatar {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    overflow: hidden;
    background: #ee4d2d; /* Shopee brand color */
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.sc-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.sc-meta h4 {
    margin: 0 0 3px 0;
    font-size: 1rem;
    font-weight: 700;
}
.sc-stars {
    color: #f59e0b;
    font-size: 0.9rem;
}
.sc-body {
    margin-bottom: 15px;
}
.sc-default {
    font-size: 0.95rem;
    color: var(--text-dark);
    margin-bottom: 12px;
    line-height: 1.5;
}
.sc-product {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(0,0,0,0.02);
    padding: 10px;
    border-radius: var(--radius-sm);
    border: 1px dashed var(--border-color);
}
.sc-product img {
    width: 50px;
    height: 50px;
    border-radius: 6px;
    object-fit: cover;
    border: 1px solid var(--border-color);
    flex-shrink: 0;
}
.sc-p-info {
    display: flex;
    flex-direction: column;
}
.sc-p-name {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-dark);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.3;
}
.sc-p-model {
    font-size: 0.75rem;
    color: var(--text-gray);
    margin-top: 4px;
}
.sc-reply {
    background: rgba(37, 99, 235, 0.05);
    border-left: 3px solid var(--primary);
    padding: 12px;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-size: 0.85rem;
    color: var(--text-dark);
    line-height: 1.5;
}
.sc-reply strong {
    display: block;
    font-size: 0.75rem;
    color: var(--primary);
    margin-bottom: 5px;
    text-transform: uppercase;
    font-weight: 800;
}

[data-theme="dark"] .shopee-reviews-section {
    background: #0f172a;
}
[data-theme="dark"] .shopee-comment-card {
    background: #1e293b;
    border-color: rgba(255, 255, 255, 0.05);
}
[data-theme="dark"] .sc-product {
    background: #0f172a;
    border-color: rgba(255, 255, 255, 0.1);
}
[data-theme="dark"] .sc-reply {
    color: #cbd5e1;
}
[data-theme="dark"] .sc-p-name, [data-theme="dark"] .sc-default {
    color: #e2e8f0;
}
"""

with open('assets/style.css', 'a', encoding='utf-8') as f:
    f.write(css)

print("Shopee section added successfully")
