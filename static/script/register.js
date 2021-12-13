document.getElementById('submit').addEventListener("click", validatePasswords);

function validatePasswords(event){
    var password = document.getElementById('password').value
    var confirmPassword = document.getElementById('confirmPassword').value
    if (password != confirmPassword){
        alert("Passwords doesn't match")
        document.getElementById('confirmPassword').value = ""
        document.getElementById('password').value = ""
        event.preventDefault();
    }
}