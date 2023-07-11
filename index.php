// index.php
<?php

require 'vendor/autoload.php';

use WeStacks\TeleBot\TeleBot;

$bot = new TeleBot('5203607843:AAF2W1nIsas5R2waSQD0LOyeIrFX2GFBKK0'); // API-токен бота здесь
$bot_user = $bot->getMe();

var_dump($bot_user);