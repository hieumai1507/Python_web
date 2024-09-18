$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid =", id)
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data){
            console.log("data =", data);
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});

$('.remove-cart').click(function(e){
    e.preventDefault();  // Ngăn hành vi mặc định của thẻ <a>
    
    var id = $(this).attr("pid").toString();
    var element = this;  // Lưu trữ phần tử được nhấp vào

    $.ajax({
        type: "GET",
        url: "/removecart",  // API xóa sản phẩm
        data: {
            prod_id: id
        },
        success: function(data){
            // Cập nhật giá trị tiền trong giỏ
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;

            // Xóa mục sản phẩm khỏi giao diện DOM
            $(element).closest('.row').remove();

            // Kiểm tra xem giỏ hàng có rỗng không
            if (data.amount == 0) {
                // Nếu giỏ hàng trống, hiển thị thông báo giỏ hàng trống
                $('.cart-items').html('<h1 class="text-center mb-5">Cart is Empty</h1>');
            }
        },
        error: function(error){
            console.log("Lỗi khi xóa sản phẩm", error);
        }
    });
});

$('.plus-wishlist').click(function() {
    var id = $(this).attr("pid").toString();  // Lấy ID sản phẩm từ thuộc tính "pid"

    $.ajax({
        type: "GET",
        url: "/pluswishlist",  // URL endpoint để thêm sản phẩm vào danh sách yêu thích
        data: {
            prod_id: id  // Gửi ID sản phẩm tới server
        },
        success: function(data) {
            // Sau khi thành công, chuyển hướng tới trang chi tiết sản phẩm
            window.location.href = `http://127.0.0.1:8000/product-detail/${id}`;
        }
    });
});
$(".minus-wishlist").click(function() {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success: function(data) {
            window.location.href = `http://127.0.0.1:8000/product-detail/${id}`;
        }
    });
});