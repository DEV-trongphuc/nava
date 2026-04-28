import re

with open('assets/style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

old_media_query = """@media (max-width: 768px) {
    .shopee-rating-summary {
        flex-direction: column;
        gap: 20px;
    }
    .sr-overview-card {
        flex: auto;
    }
    .shopee-comment-item {
        flex-direction: column;
        gap: 20px;
        padding: 25px;
    }
    .sc-reply-box {
        max-width: 100%;
    }
}"""

new_media_query = """@media (max-width: 768px) {
    .shopee-rating-summary {
        flex-direction: column;
        gap: 15px;
        margin-bottom: 30px;
    }
    .sr-overview-card, .sr-distribution-card {
        padding: 20px;
        flex: auto;
    }
    .sr-score {
        font-size: 3.5rem;
    }
    .sr-stars i {
        font-size: 1.4rem;
    }
    .sr-card-title {
        font-size: 0.9rem;
        margin-bottom: 10px;
    }
    .sr-bar-row {
        margin-bottom: 10px;
    }
    .sr-progress {
        height: 6px;
    }
    .shopee-comment-item {
        flex-direction: column;
        gap: 15px;
        padding: 20px;
    }
    .sc-reply-box {
        max-width: 100%;
    }
}"""

css_content = css_content.replace(old_media_query, new_media_query)

with open('assets/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Applied compact mobile styles.")
