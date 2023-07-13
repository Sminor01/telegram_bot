// index.php
<?php

require 'vendor/autoload.php';

use WeStacks\TeleBot\TeleBot;

$bot = new TeleBot('#'); // API-токен бота здесь
$bot_user = $bot->getMe();

var_dump($bot_user);
