const date = new Date();
document.querySelector(".year").innerHTML = date.getFullYear();

setTimeout(function () {
  $("#message").fadeOut("slow"); // remove messages automatically 
}, 3000);