document.addEventListener("DOMContentLoaded", function() {
    Array.from(document.querySelectorAll(".rte iframe")).forEach(iframe => {
        const wrapper = document.createElement("div");
        wrapper.className = "embed-responsive embed-responsive-16by9";
        iframe.parentNode.insertBefore(wrapper, iframe);
        wrapper.appendChild(iframe);
    });

    document.querySelectorAll(".rte").forEach(e => {
        contentLazy(e); // Chỉ gọi lazyload cho img, không xử lý iframe nữa
    });
});

function contentLazy(e) {
    const imgs = e.querySelectorAll("img");

    imgs.forEach(img => {
        if (!img.hasAttribute("data-src")) {
            let src = img.getAttribute("src") || "";
            img.removeAttribute("src");
            img.setAttribute("data-src", src);
            img.setAttribute("class", "lazy");
            img.setAttribute("decoding", "async");
            if (typeof io !== 'undefined') {
                io.observe(img);
            }
        }
    });
}
