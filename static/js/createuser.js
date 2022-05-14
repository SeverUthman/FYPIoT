var fnamefilled = false;
    var lnamefilled = false;

    function CheckIfUPNExists(upn)
    {
        var userexists;
        $('#userdoesexist').hide();
        $('#userdoesnotexist').hide();
        $('#spinner').show();
        $('#checkuserexistslabel').show();

        $.ajax({
                type : "GET",
                url : '/admin/checkuserexists/'+upn,
                dataType: "json",
                contentType: 'application/json;charset=UTF-8',
                success: function (data) {
                    EnableSaveButton(data)
                }
            });

    }

    function EnableSaveButton(responsecode)
    {
        $('#spinner').hide()
        $('#checkuserexistslabel').hide();
        if(responsecode == "404")
        {
            $('#savebtn').prop('disabled', false); // enable button
            $('#userdoesexist').hide();
            $('#userdoesnotexist').show();
        }
        else
        {
            $('#savebtn').prop('disabled', true); // disable button
            $('#userdoesnotexist').hide();
            $('#userdoesexist').show();
        }
    }

    function CheckIfReadyToSave()
    {
        if(fnamefilled && lnamefilled){
            
            var upn = $('#fname').val().trim() + $('#lname').val().trim() + "@sevmirazuregmail.onmicrosoft.com";
            $('#upn').val(upn);
            CheckIfUPNExists(upn);
        }
        else{
            $('#savebtn').prop('disabled', true); // disable button
        }
    }

    $(document).ready(function(){
        $('#fname').on('change', function(){
            if($('#fname').val().trim() != ""){
                fnamefilled = true;
                CheckIfReadyToSave();
            }
            else{
                fnamefilled = false;
            }
        });

        $('#lname').on('change', function(){
            if($('#lname').val().trim() != ""){
                lnamefilled = true;
                CheckIfReadyToSave();
            }
            else{
                lnamefilled = false;
            }
        });

    });