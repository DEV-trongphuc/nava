import json

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

    card = f'''                <div class="shopee-comment-card reveal">
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

# Append below testimonial section
content = content.replace('        </section>\n\n        <!-- Video Review Section -->', '        </section>\n' + new_section + '\n        <!-- Video Review Section -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Shopee section added below testimonials.")
