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
                            <div class="shopee-reply">
                                <strong>Phản hồi của Người bán:</strong>
                                <p>{reply['comment']}</p>
                            </div>'''
    else:
        reply_html = '''
                            <div class="shopee-default-text">
                                Khách hàng đã đánh giá 5 sao cho sản phẩm này.
                            </div>'''

    card = f'''                        <div class="testimonial-card">
                            <div class="testi-quote-icon"><i class="ph-fill ph-shopping-bag"></i></div>
                            <div class="testi-body">
                                <div class="shopee-product">
                                    <img src="https://cf.shopee.vn/file/{p_img}" alt="Product">
                                    <div class="sp-info">
                                        <span class="sp-name">{p_name}</span>
                                        <span class="sp-model">Phân loại: {p_model}</span>
                                    </div>
                                </div>{reply_html}
                            </div>
                            <div class="testi-header">
                                <div class="testi-avatar">{avatar_html}</div>
                                <div class="testi-info">
                                    <h4>{username}</h4>
                                    <div class="testi-stars">
                                        <i class="ph-fill ph-star"></i><i class="ph-fill ph-star"></i><i class="ph-fill ph-star"></i><i class="ph-fill ph-star"></i><i class="ph-fill ph-star"></i>
                                    </div>
                                </div>
                            </div>
                        </div>'''
    html_cards.append(card)

new_track_content = '\n'.join(html_cards)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the content of <div class="testimonial-track"> ... </div>
import re
pattern = re.compile(r'(<div class="testimonial-track">)(.*?)(</div>\s*<div class="testi-dots"></div>)', re.DOTALL)
new_content = pattern.sub(r'\1\n' + new_track_content + r'\n                    \3', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

# CSS addition
css = """
/* Shopee Reviews Styles */
.shopee-product {
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--bg-gray);
    padding: 10px;
    border-radius: var(--radius-sm);
    margin-bottom: 15px;
}
.shopee-product img {
    width: 48px;
    height: 48px;
    border-radius: 6px;
    object-fit: cover;
    flex-shrink: 0;
    border: 1px solid var(--border-color);
}
.sp-info {
    display: flex;
    flex-direction: column;
}
.sp-name {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-dark);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.3;
}
.sp-model {
    font-size: 0.75rem;
    color: var(--text-gray);
    margin-top: 4px;
}
.shopee-reply {
    background: rgba(37, 99, 235, 0.05);
    border-left: 3px solid var(--primary);
    padding: 12px;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-size: 0.85rem;
    color: var(--text-dark);
    line-height: 1.5;
}
.shopee-reply strong {
    display: block;
    font-size: 0.75rem;
    color: var(--primary);
    margin-bottom: 5px;
    text-transform: uppercase;
    font-weight: 800;
}
.shopee-default-text {
    font-size: 0.95rem;
    color: var(--text-dark);
    font-style: italic;
}
.testi-avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}

[data-theme="dark"] .shopee-product {
    background: #1e293b;
    border: 1px solid rgba(255, 255, 255, 0.05);
}
[data-theme="dark"] .sp-name {
    color: #e2e8f0;
}
[data-theme="dark"] .sp-model {
    color: #94a3b8;
}
[data-theme="dark"] .shopee-reply {
    color: #cbd5e1;
}
"""

with open('assets/style.css', 'a', encoding='utf-8') as f:
    f.write(css)

print("Reviews injected successfully")
