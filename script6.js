
            document.addEventListener("DOMContentLoaded", function () {
                document.querySelectorAll("img").forEach(function (img) {
                    if (!img.hasAttribute("alt") || img.alt.trim() === "minipc navastore maytinh #miniPC phukien egpu Minisforum MINISFORUM eGPU Laptop NavaStore") {
                        // Gán alt dựa trên tên file ảnh hoặc tiêu đề trang
                        let fileName = img.src.split('/').pop().split('.')[0];
                        img.alt = fileName.replace(/[-_]/g, ' ');
                    }
                });
            });
        