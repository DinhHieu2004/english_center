$(document).ready(function() {
    $('#changePassForm').on('submit', function(e) {
        e.preventDefault(); 
        const token = localStorage.getItem('token');

        var oldPassword = $('#oldPassword').val();
        var newPassword = $('#newPassword').val();
        var cfNewPassword = $('#cfNewPassword').val();

        if (newPassword !== cfNewPassword) {
            alert('new password and confirm new password must sample');
            return;
        }
        if (newPassword.length < 8) {
            alert('Password must be at least 8 characters ');
            return;
        }

        $.ajax({
            url: 'http://127.0.0.1:8000/api/change-password/',
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`

            },
            data: {
                current_password: oldPassword,
                new_password: newPassword,
                cf_new_password: cfNewPassword
            },
            success: function(response) {
                alert(response.message);  
                $('#ChangePassModal').modal('hide');  
            },
            error: function(xhr, status, error) {
                var errorMessage = xhr.responseJSON ? xhr.responseJSON.message : 'something happened';
                alert(errorMessage);  
            }
        });
    });
});
