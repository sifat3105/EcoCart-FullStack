$(document).ready(function() {
    $("#loadMore").on('click', function(event) {
        event.preventDefault(); // Prevent any default button behavior
        
        var _currentProduct = $('.product-box').length;
        var _limit = $(this).attr('limit-data');
        var _total = $(this).attr('total-data');
        
        console.log("Current products:", _currentProduct);
        console.log("Limit per load:", _limit);
        console.log("Total products:", _total);
        $.ajax({
            url: '/load-more',
            data: {
                limit: _limit,
                offset: _currentProduct
            },
            dataType: 'json',
            beforeSend: function() {
                $('#loadMore').attr('disabled', true);
            },
            success: function(res) {
                // Ensure that the new products are appended without causing overlap
                $('#productGrid').append(res.data);
                $('#loadMore').attr('disabled', false);
            },
            error: function() {
                $('#loadMore').attr('disabled', false);
            }
        });
        
    });
});
