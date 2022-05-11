function HandleAppliancesForKitchenResponse(data)
{
    $.each(data, function(i, obj) {
        $('#appliancetypedropdown').append("<a value='"+obj.id+"' class='dropdown-item' href='#'> "+obj.name+"</a>");
    });
}

$(document).ready(function(){
    $('#kitchendropdown a').click(function(){
            var selVal = $(this).attr('value');
            var selText = $(this).text()

            $('#kitchenid').val(selVal);
            $('#namept1').val(selText.split(" ").join(""));
            $('#kitchendd').text(selText);

            
            $.ajax({
                type : "GET",
                url : '/iot/applianceforkitchen/'+selVal,
                dataType: "json",
                data:"hi",
                contentType: 'application/json;charset=UTF-8',
                success: function (data) {
                    HandleAppliancesForKitchenResponse(data);
                    }
            });
    });

    // Need a delegated selector here because the elements of the appliance dropdow
    // are created after the page loads and don't have an event trigger for click
    $('#appliancetypedropdown').on("click", "a", function(){
            var selVal = $(this).attr('value');
            var selText = $(this).text()

            $('#applianceid').val(selVal);
            $('#namept2').val(selText);
            $('#appliancedd').text(selText);
            $('#savebutton').prop('disabled', false);
    });


    
    $('.dropdown-menu a').click(function(){
        var selText = $(this).attr('value');
        console.log("-----------------" + selText);
        $('#kitchenid').val(selText);
        });

        // Need a delegated selector here because the elements of the appliance dropdow
        // are created after the page loads and don't have an event trigger for click
        $('#appliancedropdown').on("click", "a", function(){
                var selVal = $(this).attr('value');
                var selText = $(this).text()

                $('#appliancedd').text(selText);

        });

});
