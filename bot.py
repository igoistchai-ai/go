#!/usr/bin/env python3
"""
GIFTER — one-file Telegram Stars bot + web interface, Python 3.12+.

ЧТО ЭТО
  Визуальная реплика показанного интерфейса. Переводы в ней — DEMO.
  Реальные операции: Telegram Stars -> персональный ключ доступа;
  поиск публичных пользователей Roblox и загрузка их аватаров.
  Сервис НЕ отправляет Robux, не читает баланс Roblox и не просит cookie
  или пароль Roblox. Это явно написано до покупки и при демонстрации.
  Страница входа: адаптивный CSS, светлая/тёмная тема, ввод/вставка ключа,
  анимации проверки и успешного входа. Без внешних шрифтов и CSS-библиотек.
  Все SVG-иконки, CSS/JS, фоновые рисунки и баннер бота встроены ниже.
  Аватары реальных игроков загружаются по API: их нельзя заранее встроить все.

GITHUB -> RENDER (один исходный файл bot.py)
  1. Создать private GitHub repo и загрузить только этот bot.py.
  2. Render -> New -> Web Service -> подключить этот repo -> Python 3.
     Build Command: pip install 'aiohttp>=3.14.4,<4' 'psycopg[binary]>=3.2,<4'
     Start Command: python bot.py
     Health Check Path: /healthz
     Instance count: 1. Сервер слушает 0.0.0.0:$PORT (по умолчанию 10000).
  3. Environment (секреты НЕ помещать в GitHub):
     BOT_TOKEN         — токен @BotFather
     APP_SECRET        — постоянная случайная строка >=32 символов;
                         создать: python -c 'import secrets; print(secrets.token_urlsafe(48))'
     ADMIN_ID          — числовой Telegram ID главного администратора
     OWNER_IDS         — необязательно: дополнительные admin ID через запятую
                         (старые настройки OWNER_IDS продолжают работать)
     PUBLIC_URL        — https://имя.onrender.com (или RENDER_EXTERNAL_URL)
     DATABASE_URL      — постоянная PostgreSQL БД (URL от провайдера).
     SUPPORT_USERNAME  — необязательно: username поддержки, без @
     GROUP_CHAT_ID     — необязательно: -100... ID супергруппы/канала
     GROUP_INVITE_URL  — необязательно: https://t.me/... ссылка на общий чат
     STAR_EMOJI_ID     — необязательно: custom emoji ID, если доступен боту.
     TELEGRAM_TEST     — 1 только для отдельного тестового бота Telegram.
  4. Вместо PostgreSQL можно платный persistent disk Render:
     mount /var/data; SQLITE_PATH=/var/data/gifter.sqlite3;
     PERSISTENT_SQLITE=1. Без постоянной БД боевой запуск на Render запрещён,
     чтобы платные ключи не потерялись при перезапуске.
  5. Бот сам регистрирует webhook и кнопку Mini App. Для запуска вне Telegram
     открыть PUBLIC_URL и ввести ключ из /key. Ключ — секрет доступа.
     Не менять APP_SECRET после продаж: из него восстанавливаются ключи.
  6. В общей супергруппе сделать бота админом (удалять сообщения,
     ограничивать участников), затем владельцу отправить /lockchat боту
     в ЛС. Обычные участники не смогут писать; сообщения других людей
     бот удаляет. Владелец/админы Telegram всё равно имеют свои права.
     Для канала достаточно дать боту право публикации; /lockchat не нужен.

24/7
  Открытый PORT и GitHub не отменяют сон бесплатного Render. /healthz готов
  для внешнего монитора доступности (GET PUBLIC_URL/healthz каждые 5 минут).
  Внешние HTTP-проверки создают входящий
  трафик, но не гарантируют 24/7, не отменяют квоты и остановки Render.
  Для платёжного бота используйте instance без idle spin-down: холодный
  старт Free может не уложиться в 10 секунд Telegram pre-checkout.
  Самопинг из спящего процесса не работает; фиктивной гарантии здесь нет.

КОМАНДЫ
  /start /stars /app /key /status /settings /find username /terms /privacy /paysupport
  /paysupport текст — передать вопрос владельцу, /cancel — отменить ввод.
  Администратор: /admin /lockchat /refund ORDER_ID (с подтверждением).
  /give 1m|1h|1d|1w|lifetime — бесплатно выдать ключ самому админу.
  /give 2h TELEGRAM_ID — выдать ключ этому пользователю; также можно ответить
  /give 2h на его сообщение в GROUP_CHAT_ID. Ключи отправляются только в ЛС.
  Для получения сообщений пользователь должен ранее отправить боту /start.
  ADMIN_ID=123456789 — ID человека, не токен бота и не @username.
  /start -> Настроить панель -> Демо-баланс / Ник -> Сохранить.
  Настройки индивидуальны, доступны при действующем (в т.ч. ещё не
  активированном) ключе и сохраняются в БД. Срок при настройке не запускается.
  Ник — до 32 видимых символов; демо-баланс — 0..9 999 999 999.
  Сервер блокирует просроченные сессии при каждом запросе; браузер закрывает
  панель таймером по серверному времени, проверяя срок также при возвращении.
  Сохранённые настройки обновляются при открытии / возврате в панель и
  каждые 15 секунд, если она уже открыта. Lifetime не имеет срока ключа;
  браузерная сессия живёт не более 7 дней, затем нужен повторный вход.
  Таблицы настроек создаются автоматически, существующие оплаты не меняются.
  Цены: 1ч=5, 2ч=15, 1д=30, 2д=50, 5д=100, навсегда=400 Stars.
  Срок начинается при первой активации. Повторная оплата создаёт отдельный
  ключ, а не продлевает старый. Возврат отзывает соответствующий ключ.

ЛОКАЛЬНО
  pip install 'aiohttp>=3.14.4,<4'
  python bot.py --preview       # localhost:10000, вход DEMO-LOCAL
  python bot.py --self-test     # без сети, тесты платежей/ключей/гонок
  Preview имеет отдельную временную БД, не принимает Stars и не шлёт в TG.

ПРОВЕРКА ЭТОЙ СБОРКИ
  Проверены Python/JavaScript-синтаксис и встроенные локальные тесты.
  Настоящие платежи Telegram, PostgreSQL и Render не запускались без ваших
  настроек. Запросы к Roblox из среды сборки недоступны по сети.
  Браузерная визуальная проверка заблокирована средой; точное совпадение
  пиксель в пиксель с роликом не подтверждено. Перед продажами обязательно
  проверьте весь путь на отдельном тестовом боте, включая возврат.

API
  GET  /healthz, /api/config, /api/me, /api/users?q=, /api/user/{id},
       /api/avatar/{id}, /api/history
  POST /api/activate {key}, /api/telegram {init_data}, /api/logout,
       /api/demo-gifts {recipient_id, amount, request_id}
  POST /telegram/webhook — только с Telegram secret header.
  Авторизация: HttpOnly session cookie или bearer в памяти вкладки (для
  Telegram Web без сторонних cookie), проверка срока на каждом запросе.
  Покупки, входящие updates и исходящие сообщения сохраняются в БД.
  Exactly-once выдача ключа по charge_id. Доставка сообщений — at-least-once:
  сбой после отправки до фиксации может повторить сообщение, но не покупку.
  Данные: ID покупателя, платежи, hash ключа, сессии и история DEMO.
  /privacy сообщает это пользователю. Правила/поддержку адаптируйте под себя
  до реального запуска; проверьте тестовую оплату и возврат в Telegram.

ОФИЦИАЛЬНЫЕ ИСТОЧНИКИ (проверены 2026-10-17)
  https://core.telegram.org/bots/payments-stars
  https://core.telegram.org/bots/api
  https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
  https://render.com/docs/free
  https://render.com/docs/web-services#port-binding
  https://create.roblox.com/docs/cloud/reference/domains/users
  https://create.roblox.com/docs/cloud/reference/features/thumbnails
  https://en.help.roblox.com/hc/en-us/articles/48510707796756-Sending-and-Receiving-Robux
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import hmac
import html
import io
import json
import logging
import os
import re
import secrets
import sqlite3
import tempfile
import threading
import time
import unittest
import unicodedata
from collections import OrderedDict, defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

from aiohttp import ClientSession, ClientTimeout, FormData, web

LOG = logging.getLogger("gifter")
PLANS = {
    "1h": {"label": "1 час", "stars": 5, "seconds": 3600},
    "2h": {"label": "2 часа", "stars": 15, "seconds": 7200},
    "1d": {"label": "1 день", "stars": 30, "seconds": 86400},
    "2d": {"label": "2 дня", "stars": 50, "seconds": 172800},
    "5d": {"label": "5 дней", "stars": 100, "seconds": 432000},
    "forever": {"label": "Навсегда", "stars": 400, "seconds": None},
}
DEMO_BALANCE = 1_000_000
MAX_DEMO_BALANCE = 9_999_999_999
DEFAULT_NICKNAME = "Gifter Studio"
SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
 id TEXT PRIMARY KEY, user_id BIGINT NOT NULL, plan TEXT NOT NULL,
 stars INTEGER NOT NULL, duration BIGINT, created_at BIGINT NOT NULL,
 status TEXT NOT NULL DEFAULT 'pending', charge_id TEXT UNIQUE, paid_at BIGINT
);
CREATE TABLE IF NOT EXISTS licenses (
 key_hash TEXT PRIMARY KEY, order_id TEXT UNIQUE NOT NULL REFERENCES orders(id),
 owner_id BIGINT NOT NULL, duration BIGINT, activated_at BIGINT,
 expires_at BIGINT, revoked INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS sessions (
 token_hash TEXT PRIMARY KEY, key_hash TEXT NOT NULL REFERENCES licenses(key_hash),
 expires_at BIGINT NOT NULL
);
CREATE TABLE IF NOT EXISTS wallets (
 owner_id BIGINT PRIMARY KEY, balance BIGINT NOT NULL
);
CREATE TABLE IF NOT EXISTS profiles (
 owner_id BIGINT PRIMARY KEY, nickname TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS profile_drafts (
 user_id BIGINT PRIMARY KEY, draft_id TEXT NOT NULL,
 key_hash TEXT NOT NULL REFERENCES licenses(key_hash),
 balance BIGINT NOT NULL, nickname TEXT NOT NULL,
 balance_changed INTEGER NOT NULL DEFAULT 0, nickname_changed INTEGER NOT NULL DEFAULT 0,
 awaiting TEXT NOT NULL DEFAULT '', expires_at BIGINT NOT NULL
);
CREATE TABLE IF NOT EXISTS license_grants (
 order_id TEXT PRIMARY KEY REFERENCES orders(id), admin_id BIGINT NOT NULL,
 event_id TEXT UNIQUE NOT NULL, created_at BIGINT NOT NULL
);
CREATE TABLE IF NOT EXISTS gifts (
 id TEXT PRIMARY KEY, owner_id BIGINT NOT NULL, recipient_id BIGINT NOT NULL,
 recipient_name TEXT NOT NULL, amount BIGINT NOT NULL, created_at BIGINT NOT NULL,
 request_id TEXT NOT NULL, balance_after BIGINT NOT NULL,
 UNIQUE(owner_id, request_id)
);
CREATE TABLE IF NOT EXISTS inbox (
 id BIGINT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending',
 attempts INTEGER NOT NULL DEFAULT 0, lease BIGINT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS outbox (
 id TEXT PRIMARY KEY, method TEXT NOT NULL, payload TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'pending', attempts INTEGER NOT NULL DEFAULT 0,
 lease BIGINT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS payment_incidents (
 charge_id TEXT PRIMARY KEY, user_id BIGINT NOT NULL,
 order_id TEXT NOT NULL, amount BIGINT NOT NULL, reason TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS support_pending (user_id BIGINT PRIMARY KEY, expires_at BIGINT NOT NULL);
CREATE INDEX IF NOT EXISTS licenses_owner ON licenses(owner_id);
CREATE INDEX IF NOT EXISTS gifts_owner ON gifts(owner_id, created_at);
CREATE INDEX IF NOT EXISTS inbox_pending ON inbox(status, lease);
CREATE INDEX IF NOT EXISTS outbox_pending ON outbox(status, lease);
"""


def now():
    return int(time.time())


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def key_for(order_id, secret):
    encoded = base64.b32encode(hmac.digest(secret.encode(), ("key:" + order_id).encode(), "sha256")).decode()[:30]
    return "GF-" + "-".join(encoded[i:i + 6] for i in range(0, 30, 6))


def utc(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%d.%m.%Y %H:%M:%S UTC") if ts else "не активирован"


def grant_duration(value):
    value = value.strip().lower()
    if value == "lifetime":
        return None, "Навсегда"
    match = re.fullmatch(r"([1-9][0-9]{0,5})([mhdw])", value)
    if match:
        n, unit = int(match[1]), match[2]
        seconds = n * {"m": 60, "h": 3600, "d": 86400, "w": 604800}[unit]
        if seconds <= 3650 * 86400:
            return seconds, f"{n} {dict(m='мин.', h='ч.', d='дн.', w='нед.')[unit]}"
    raise ValueError("Срок: 1m, 1h, 1d, 1w или lifetime. Можно указать число: 30m, 2h, 7d. Максимум — 3650 дней.")


def plan_label(plan_id):
    if plan_id in PLANS:
        return PLANS[plan_id]["label"]
    if plan_id.startswith("grant:"):
        return grant_duration(plan_id[6:])[1] + " · выдан админом"
    return "Доступ"


def validate_nickname(value):
    value = value.strip()
    if not 1 <= len(value) <= 32 or any(unicodedata.category(c).startswith("C") for c in value):
        raise ValueError("Ник: от 1 до 32 видимых символов, без переносов строк.")
    return value


def validate_demo_balance(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9\s,]{1,40}", value):
        raise ValueError("Пришлите целое неотрицательное число, например 1000000.")
    digits = re.sub(r"[\s,]", "", value)
    if not digits or len(digits) > 10 or int(digits) > MAX_DEMO_BALANCE:
        raise ValueError("Демо-баланс: от 0 до 9 999 999 999.")
    return int(digits)


def verify_init_data(raw, token, clock=None):
    if not isinstance(raw, str) or len(raw) > 16000:
        raise ValueError("Неверные данные Telegram")
    items = parse_qsl(raw, keep_blank_values=True, strict_parsing=True)
    fields = dict(items)
    if len(fields) != len(items):
        raise ValueError("Повторяющиеся поля")
    supplied = fields.pop("hash", "")
    check = "\n".join(f"{k}={fields[k]}" for k in sorted(fields))
    secret = hmac.digest(b"WebAppData", token.encode(), "sha256")
    expected = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, supplied):
        raise ValueError("Подпись Telegram не прошла проверку")
    age = (now() if clock is None else clock) - int(fields.get("auth_date", 0))
    if not -30 <= age <= 3600:
        raise ValueError("Откройте Mini App заново: данные входа устарели")
    user = json.loads(fields.get("user", "{}"))
    if type(user.get("id")) is not int or user["id"] <= 0:
        raise ValueError("Не найден пользователь Telegram")
    return user


@dataclass
class Config:
    token: str = ""
    secret: str = ""
    public_url: str = ""
    database_url: str = ""
    sqlite_path: str = "gifter.sqlite3"
    owners: tuple = ()
    admin_id: int = 0
    group_id: int = 0
    group_url: str = ""
    support: str = ""
    star_emoji: str = ""
    preview: bool = False
    test: bool = False
    port: int = 10000

    @classmethod
    def from_env(cls, preview=False):
        return cls(
            token=os.getenv("BOT_TOKEN", "").strip(), secret=os.getenv("APP_SECRET", "").strip(),
            public_url=os.getenv("PUBLIC_URL", os.getenv("RENDER_EXTERNAL_URL", "")).rstrip("/"),
            database_url=os.getenv("DATABASE_URL", ""), sqlite_path=os.getenv("SQLITE_PATH", "gifter.sqlite3"),
            owners=tuple(int(x.strip()) for x in os.getenv("OWNER_IDS", "").split(",") if x.strip()),
            admin_id=int(os.getenv("ADMIN_ID", os.getenv("admin_id", "0")) or "0"),
            group_id=int(os.getenv("GROUP_CHAT_ID", "0")), group_url=os.getenv("GROUP_INVITE_URL", ""),
            support=os.getenv("SUPPORT_USERNAME", "").lstrip("@"), star_emoji=os.getenv("STAR_EMOJI_ID", ""),
            preview=preview, test=os.getenv("TELEGRAM_TEST") == "1", port=int(os.getenv("PORT", "10000")),
        )

    def validate(self):
        if self.preview:
            return
        if not re.fullmatch(r"\d+:[A-Za-z0-9_-]+", self.token):
            raise ValueError("Задайте BOT_TOKEN из @BotFather")
        if len(self.secret) < 32 or not self.admin_ids or any(x <= 0 for x in self.admin_ids):
            raise ValueError("Нужны постоянный APP_SECRET (>=32 символов) и ADMIN_ID (числовой Telegram ID)")
        p = urlsplit(self.public_url)
        if p.scheme != "https" or not p.hostname or p.path or p.query or p.fragment or p.username:
            raise ValueError("PUBLIC_URL должен быть HTTPS origin без пути")
        if os.getenv("RENDER") and not self.database_url and os.getenv("PERSISTENT_SQLITE") != "1":
            raise ValueError("На Render нужна DATABASE_URL или persistent disk + PERSISTENT_SQLITE=1")
        if self.support and not re.fullmatch(r"[A-Za-z0-9_]{5,32}", self.support):
            raise ValueError("SUPPORT_USERNAME: username без @")
        if self.group_url and not self.group_url.startswith("https://t.me/"):
            raise ValueError("GROUP_INVITE_URL должен начинаться с https://t.me/")

    @property
    def admin_ids(self):
        return tuple(dict.fromkeys(((self.admin_id,) if self.admin_id else ()) + self.owners))

    @property
    def webhook_secret(self):
        return hmac.new(self.secret.encode(), b"telegram-webhook", hashlib.sha256).hexdigest()


class Tx:
    def __init__(self, conn, pg=False):
        self.conn, self.pg = conn, pg

    def execute(self, sql, args=()):
        return self.conn.execute(sql.replace("?", "%s") if self.pg else sql, args)

    def one(self, sql, args=(), lock=False):
        row = self.execute(sql + (" FOR UPDATE" if lock and self.pg else ""), args).fetchone()
        return dict(row) if row else None

    def all(self, sql, args=()):
        return [dict(x) for x in self.execute(sql, args).fetchall()]

    def enqueue(self, identifier, method, payload):
        self.execute("INSERT INTO outbox(id,method,payload) VALUES(?,?,?) ON CONFLICT(id) DO NOTHING",
                     (identifier, method, json.dumps(payload, ensure_ascii=False)))


class Database:
    def __init__(self, cfg):
        self.cfg, self.lock, self.pg_conn = cfg, threading.RLock(), None
        if not cfg.database_url:
            Path(cfg.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
        self.run_sync(lambda tx: [tx.execute(stmt) for stmt in SCHEMA.split(";") if stmt.strip()])

    def run_sync(self, fn):
        with self.lock:
            if self.cfg.database_url:
                import psycopg
                from psycopg.rows import dict_row
                if self.pg_conn is None or self.pg_conn.closed:
                    self.pg_conn = psycopg.connect(self.cfg.database_url, row_factory=dict_row,
                                                   autocommit=True, connect_timeout=5)
                try:
                    with self.pg_conn.transaction():
                        return fn(Tx(self.pg_conn, True))
                except psycopg.OperationalError:
                    self.pg_conn.close()
                    raise
            conn = sqlite3.connect(self.cfg.sqlite_path, timeout=10)
            conn.row_factory = sqlite3.Row
            try:
                conn.execute("PRAGMA foreign_keys=ON")
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("BEGIN IMMEDIATE")
                value = fn(Tx(conn))
                conn.commit()
                return value
            except BaseException:
                conn.rollback()
                raise
            finally:
                conn.close()

    async def run(self, fn):
        return await asyncio.to_thread(self.run_sync, fn)

    def close(self):
        if self.pg_conn is not None:
            self.pg_conn.close()


class Store:
    def __init__(self, cfg, db):
        self.cfg, self.db = cfg, db

    def order(self, tx, user_id, plan_id):
        plan = PLANS[plan_id]
        oid = secrets.token_hex(12)
        tx.execute("INSERT INTO orders(id,user_id,plan,stars,duration,created_at) VALUES(?,?,?,?,?,?)",
                   (oid, user_id, plan_id, plan["stars"], plan["seconds"], now()))
        return tx.one("SELECT * FROM orders WHERE id=?", (oid,))

    def grant(self, tx, admin_id, user_id, duration, event):
        if admin_id not in self.cfg.admin_ids:
            raise PermissionError("Команда /give доступна только ADMIN_ID.")
        if type(user_id) is not int or not 0 < user_id < 2**52:
            raise ValueError("Нужен положительный числовой Telegram ID пользователя.")
        duration = duration.strip().lower()
        seconds, _ = grant_duration(duration)
        oid = "grant_" + digest(event)[:24]
        existing = tx.one("SELECT * FROM orders WHERE id=?", (oid,))
        if existing:
            return existing
        tx.execute("INSERT INTO orders(id,user_id,plan,stars,duration,created_at,status,paid_at) VALUES(?,?,?,0,?,?,'granted',?)",
                   (oid, user_id, "grant:" + duration, seconds, now(), now()))
        tx.execute("INSERT INTO licenses(key_hash,order_id,owner_id,duration) VALUES(?,?,?,?)",
                   (digest(key_for(oid, self.cfg.secret)), oid, user_id, seconds))
        tx.execute("INSERT INTO license_grants(order_id,admin_id,event_id,created_at) VALUES(?,?,?,?)",
                   (oid, admin_id, event, now()))
        tx.execute("INSERT INTO wallets(owner_id,balance) VALUES(?,?) ON CONFLICT DO NOTHING", (user_id, DEMO_BALANCE))
        return tx.one("SELECT * FROM orders WHERE id=?", (oid,))

    def available_license(self, tx, uid):
        rows = tx.all("SELECT l.*,o.paid_at FROM licenses l JOIN orders o ON o.id=l.order_id WHERE l.owner_id=? AND l.revoked=0 ORDER BY o.paid_at DESC", (uid,))
        active = [r for r in rows if r["activated_at"] is not None and (r["expires_at"] is None or r["expires_at"] > now())]
        active.sort(key=lambda r: r["expires_at"] or 2**62, reverse=True)
        pending = [r for r in reversed(rows) if r["activated_at"] is None]
        return (active or pending or [None])[0]

    def profile(self, tx, uid):
        wallet = tx.one("SELECT balance FROM wallets WHERE owner_id=?", (uid,))
        profile = tx.one("SELECT nickname FROM profiles WHERE owner_id=?", (uid,))
        return {"balance": wallet["balance"] if wallet else DEMO_BALANCE,
                "nickname": profile["nickname"] if profile else DEFAULT_NICKNAME}

    def open_profile(self, tx, uid, event):
        row = self.available_license(tx, uid)
        if not row:
            raise ValueError("Нет действующего ключа. Получите доступ через /stars или у администратора.")
        draft_id = digest("profile:" + event)[:12]
        existing = tx.one("SELECT * FROM profile_drafts WHERE user_id=? AND draft_id=?", (uid, draft_id))
        if existing:
            return self.profile_draft(tx, uid, draft_id)
        data = self.profile(tx, uid)
        tx.execute("DELETE FROM support_pending WHERE user_id=?", (uid,))
        tx.execute("INSERT INTO profile_drafts(user_id,draft_id,key_hash,balance,nickname,expires_at) VALUES(?,?,?,?,?,?) "
                   "ON CONFLICT(user_id) DO UPDATE SET draft_id=excluded.draft_id,key_hash=excluded.key_hash,balance=excluded.balance,"
                   "nickname=excluded.nickname,expires_at=excluded.expires_at,balance_changed=0,nickname_changed=0,awaiting=''",
                   (uid, draft_id, row["key_hash"], data["balance"], data["nickname"], now() + 1800))
        return self.profile_draft(tx, uid, draft_id)

    def profile_draft(self, tx, uid, draft_id):
        draft = tx.one("SELECT * FROM profile_drafts WHERE user_id=? AND draft_id=?", (uid, draft_id), lock=True)
        if not draft or draft["expires_at"] <= now():
            raise ValueError("Эта форма устарела. Откройте /settings заново.")
        row = tx.one("SELECT * FROM licenses WHERE key_hash=? AND owner_id=?", (draft["key_hash"], uid))
        if not row or row["revoked"] or (row["expires_at"] is not None and row["expires_at"] <= now()):
            raise ValueError("Срок ключа истёк или ключ отозван. Изменения не сохранены.")
        return draft

    def await_profile_field(self, tx, uid, draft_id, field):
        if field not in ("balance", "nickname"):
            raise ValueError("Неизвестная настройка")
        self.profile_draft(tx, uid, draft_id)
        tx.execute("UPDATE profile_drafts SET awaiting=? WHERE user_id=? AND draft_id=?", (field, uid, draft_id))

    def edit_profile(self, tx, uid, text, event):
        marker = "profile-edit:" + event
        done = tx.one("SELECT value FROM settings WHERE key=?", (marker,))
        if done:
            return json.loads(done["value"])
        pending = tx.one("SELECT * FROM profile_drafts WHERE user_id=?", (uid,))
        if not pending or not pending["awaiting"]:
            return None
        draft = self.profile_draft(tx, uid, pending["draft_id"])
        field = draft["awaiting"]
        if field == "balance":
            value = validate_demo_balance(text)
        elif field == "nickname":
            value = validate_nickname(text)
        else:
            return None
        # Only these two validated column names can enter SQL.
        tx.execute(f"UPDATE profile_drafts SET {field}=?,{field}_changed=1,awaiting='' WHERE user_id=?", (value, uid))
        draft = self.profile_draft(tx, uid, draft["draft_id"])
        tx.execute("INSERT INTO settings(key,value) VALUES(?,?)", (marker, json.dumps(draft, ensure_ascii=False)))
        return draft

    def save_profile(self, tx, uid, draft_id, event):
        marker = "profile-save:" + event
        done = tx.one("SELECT value FROM settings WHERE key=?", (marker,))
        if done:
            return json.loads(done["value"])
        draft = self.profile_draft(tx, uid, draft_id)
        if draft["awaiting"]:
            raise ValueError("Сначала отправьте новое значение текстовым сообщением или отмените ввод через /cancel.")
        if draft["balance_changed"]:
            tx.execute("INSERT INTO wallets(owner_id,balance) VALUES(?,?) ON CONFLICT(owner_id) DO UPDATE SET balance=excluded.balance", (uid, draft["balance"]))
        if draft["nickname_changed"]:
            tx.execute("INSERT INTO profiles(owner_id,nickname) VALUES(?,?) ON CONFLICT(owner_id) DO UPDATE SET nickname=excluded.nickname", (uid, draft["nickname"]))
        data = self.profile(tx, uid)
        tx.execute("DELETE FROM profile_drafts WHERE user_id=? AND draft_id=?", (uid, draft_id))
        tx.execute("INSERT INTO settings(key,value) VALUES(?,?)", (marker, json.dumps(data, ensure_ascii=False)))
        return data

    def precheck(self, tx, query):
        row = tx.one("SELECT * FROM orders WHERE id=?", (query.get("invoice_payload", ""),))
        if not row or row["user_id"] != query.get("from", {}).get("id"):
            return "Этот счёт создан для другого пользователя. Откройте /stars."
        if query.get("currency") != "XTR" or query.get("total_amount") != row["stars"]:
            return "Сумма или валюта не совпадает. Создайте новый счёт через /stars."
        if row["status"] != "pending" or now() - row["created_at"] > 3600:
            return "Счёт оплачен или устарел. Создайте новый через /stars."
        return None

    def paid(self, tx, uid, payment):
        oid = payment.get("invoice_payload", "")
        charge = payment.get("telegram_payment_charge_id", "")
        if not isinstance(charge, str) or not charge:
            raise ValueError("Missing payment charge ID")
        duplicate = tx.one("SELECT * FROM orders WHERE charge_id=?", (charge,))
        if duplicate:
            return duplicate["id"]
        row = tx.one("SELECT * FROM orders WHERE id=?", (oid,), lock=True)
        if row and row["charge_id"] == charge and row["user_id"] == uid:
            return row["id"]
        valid = (row and row["status"] == "pending" and row["user_id"] == uid and
                 payment.get("currency") == "XTR" and payment.get("total_amount") == row["stars"])
        if not valid:
            tx.execute("INSERT INTO payment_incidents(charge_id,user_id,order_id,amount,reason) VALUES(?,?,?,?,?) ON CONFLICT DO NOTHING",
                       (charge, uid, str(oid), int(payment.get("total_amount", 0)), "Payment did not match an unpaid order"))
            for owner in self.cfg.admin_ids:
                tx.enqueue("incident:" + charge + ":" + str(owner), "sendMessage", {
                    "chat_id": owner, "text": "⚠️ Платёж требует разбора. Ключ не выдан.\n"
                    f"User: {uid}\nOrder: {oid}\nCharge: {charge}\nПроверьте payment_incidents в БД и возврат."
                })
            tx.enqueue("incident-user:" + charge, "sendMessage", {"chat_id": uid,
                "text": "Платёж получен, но не совпал со счётом. Владелец уведомлён. Обратитесь /paysupport; не платите повторно."})
            return None
        key = key_for(oid, self.cfg.secret)
        tx.execute("UPDATE orders SET status='paid',charge_id=?,paid_at=? WHERE id=?", (charge, now(), oid))
        tx.execute("INSERT INTO licenses(key_hash,order_id,owner_id,duration) VALUES(?,?,?,?)",
                   (digest(key), oid, uid, row["duration"]))
        tx.execute("INSERT INTO wallets(owner_id,balance) VALUES(?,?) ON CONFLICT DO NOTHING", (uid, DEMO_BALANCE))
        label = PLANS[row["plan"]]["label"]
        tx.enqueue("receipt:" + oid, "sendMessage", {"chat_id": uid, "parse_mode": "HTML",
            "_key_ids": [oid],
            "text": f"✅ <b>Оплата получена · {row['stars']} ⭐</b>\n\n"
                    f"Доступ: <b>{label}</b>\nКлюч:\n<code>[[key:{oid}]]</code>\n\n"
                    "Срок начнётся при первом входе. Не передавайте ключ другим.\n"
                    "Это доступ к визуальному DEMO, не покупка Robux.\n"
                    f"Заказ: <code>{oid}</code>\nПомощь: /paysupport",
            "reply_markup": {"inline_keyboard": [[{"text": "🎁 Открыть Gifter", "web_app": {"url": self.cfg.public_url}}]]}})
        if self.cfg.group_id:
            tx.enqueue("purchase:" + oid, "sendMessage", {"chat_id": self.cfg.group_id,
                "text": f"⭐ GIFTER · Новый доступ\n{label} · {row['stars']} Stars\nЗаказ #{oid[-6:]}\nКлюч доставлен покупателю лично."})
        return oid

    def refunded(self, tx, charge):
        row = tx.one("SELECT * FROM orders WHERE charge_id=?", (charge,), lock=True)
        if not row:
            return
        tx.execute("UPDATE orders SET status='refunded' WHERE id=?", (row["id"],))
        tx.execute("UPDATE licenses SET revoked=1 WHERE order_id=?", (row["id"],))
        tx.enqueue("refund-receipt:" + row["id"], "sendMessage", {"chat_id": row["user_id"],
            "text": f"↩️ Возврат {row['stars']} ⭐ выполнен. Ключ по заказу {row['id']} отозван."})

    def activate(self, tx, key, required_uid=None, clock=None):
        ts = now() if clock is None else clock
        kh = digest(key.strip().upper())
        row = tx.one("SELECT * FROM licenses WHERE key_hash=?", (kh,), lock=True)
        if not row or row["revoked"] or (required_uid and row["owner_id"] != required_uid):
            raise ValueError("Ключ не найден или отозван")
        if row["activated_at"] is None:
            expiry = ts + row["duration"] if row["duration"] is not None else None
            tx.execute("UPDATE licenses SET activated_at=?,expires_at=? WHERE key_hash=?", (ts, expiry, kh))
            row.update(activated_at=ts, expires_at=expiry)
        if row["expires_at"] is not None and row["expires_at"] <= ts:
            raise ValueError("Срок ключа истёк. Новые тарифы доступны через /stars")
        token = secrets.token_urlsafe(32)
        session_expiry = min(ts + 604800, row["expires_at"] or ts + 604800)
        tx.execute("INSERT INTO sessions(token_hash,key_hash,expires_at) VALUES(?,?,?)", (digest(token), kh, session_expiry))
        tx.execute("DELETE FROM sessions WHERE expires_at<?", (ts,))
        return token, session_expiry

    def session(self, tx, token, clock=None):
        ts = now() if clock is None else clock
        row = tx.one("SELECT l.*,s.expires_at AS session_expiry FROM sessions s JOIN licenses l ON l.key_hash=s.key_hash WHERE s.token_hash=?",
                     (digest(token),)) if token else None
        if not row or row["revoked"] or row["session_expiry"] <= ts or (row["expires_at"] is not None and row["expires_at"] <= ts):
            return None
        return row

    def gift(self, tx, token, rid, name, amount, request_id):
        license_row = self.session(tx, token)
        if not license_row:
            raise PermissionError("Сессия истекла")
        uid = license_row["owner_id"]
        previous = tx.one("SELECT * FROM gifts WHERE owner_id=? AND request_id=?", (uid, request_id))
        if previous:
            if previous["amount"] != amount or previous["recipient_id"] != rid:
                raise ValueError("ID операции уже использован для других данных")
            return previous
        if type(amount) is not int or not 1 <= amount <= MAX_DEMO_BALANCE:
            raise ValueError("Введите целое число от 1 до 9 999 999 999")
        wallet = tx.one("SELECT * FROM wallets WHERE owner_id=?", (uid,), lock=True)
        if not wallet or wallet["balance"] < amount:
            raise ValueError("Недостаточно демонстрационного баланса")
        # Lock serializes concurrent gifts. Recheck idempotency after acquiring it.
        previous = tx.one("SELECT * FROM gifts WHERE owner_id=? AND request_id=?", (uid, request_id))
        if previous:
            if previous["amount"] != amount or previous["recipient_id"] != rid:
                raise ValueError("ID операции уже использован для других данных")
            return previous
        balance = wallet["balance"] - amount
        tx.execute("UPDATE wallets SET balance=? WHERE owner_id=?", (balance, uid))
        gid = secrets.token_hex(12)
        tx.execute("INSERT INTO gifts(id,owner_id,recipient_id,recipient_name,amount,created_at,request_id,balance_after) VALUES(?,?,?,?,?,?,?,?)",
                   (gid, uid, rid, name, amount, now(), request_id, balance))
        return tx.one("SELECT * FROM gifts WHERE id=?", (gid,))


class TelegramError(Exception):
    def __init__(self, code, description, retry_after=0):
        self.code, self.description, self.retry_after = code, description, retry_after
        super().__init__(f"Telegram error {code}")  # Never include token/URL in logs.


class Telegram:
    def __init__(self, cfg, http):
        self.cfg, self.http, self.username, self.id = cfg, http, "", 0

    async def call(self, method, payload, media=None):
        suffix = "/test/" if self.cfg.test else "/"
        url = f"https://api.telegram.org/bot{self.cfg.token}{suffix}{method}"
        kwargs = {"json": payload}
        if media:
            form = FormData()
            for k, v in payload.items():
                form.add_field(k, json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list, bool)) else str(v))
            form.add_field("photo", media, filename="gifter.png", content_type="image/png")
            kwargs = {"data": form}
        async with self.http.post(url, **kwargs, timeout=ClientTimeout(total=15)) as response:
            data = await response.json(content_type=None)
            if not data.get("ok"):
                raise TelegramError(data.get("error_code", response.status), data.get("description", ""),
                                    data.get("parameters", {}).get("retry_after", 0))
            return data.get("result")


class Roblox:
    def __init__(self, http):
        self.http, self.cache, self.sem = http, OrderedDict(), asyncio.Semaphore(5)

    def cached(self, key):
        entry = self.cache.get(key)
        if entry and entry[0] > time.monotonic():
            self.cache.move_to_end(key)
            return entry[1]
        return None

    def put(self, key, value, ttl=120):
        self.cache[key] = (time.monotonic() + ttl, value)
        self.cache.move_to_end(key)
        while len(self.cache) > 512:
            self.cache.popitem(last=False)
        return value

    async def fetch(self, host, path, method="GET", **kwargs):
        async with self.sem:
            async with self.http.request(method, f"https://{host}{path}", timeout=ClientTimeout(total=8), **kwargs) as response:
                if response.status == 429:
                    raise ValueError("Roblox ограничил запросы. Повторите немного позже.")
                if response.status == 404:
                    raise ValueError("Пользователь Roblox не найден")
                if response.status != 200:
                    raise ValueError("Roblox API временно недоступен")
                return await response.json(content_type=None)

    async def search(self, query):
        query = query.strip().lstrip("@")
        if not (re.fullmatch(r"[A-Za-z0-9_]{3,32}", query) or re.fullmatch(r"\d{1,14}", query)):
            raise ValueError("Введите username из 3–32 букв, цифр или _, либо числовой ID")
        cache_key = "search:" + query.lower()
        cached = self.cached(cache_key)
        if cached is not None:
            return cached
        if query.isdigit():
            rows = [await self.user(int(query))]
        else:
            exact = await self.fetch("users.roblox.com", "/v1/usernames/users", "POST",
                                     json={"usernames": [query], "excludeBannedUsers": True})
            rows = exact.get("data", [])
            if not rows:
                result = await self.fetch("users.roblox.com", "/v1/users/search", params={"keyword": query, "limit": "10"})
                rows = result.get("data", [])
        return self.put(cache_key, [{"id": int(x["id"]), "name": x.get("name", ""),
            "displayName": x.get("displayName", x.get("name", "")), "hasVerifiedBadge": bool(x.get("hasVerifiedBadge"))} for x in rows[:10]])

    async def user(self, uid):
        if not 1 <= uid <= 10**14:
            raise ValueError("Неверный ID пользователя")
        key = "user:" + str(uid)
        cached = self.cached(key)
        if cached is not None:
            return cached
        row = await self.fetch("users.roblox.com", f"/v1/users/{uid}")
        if row.get("isBanned"):
            raise ValueError("Этот аккаунт недоступен")
        return self.put(key, {"id": uid, "name": row["name"], "displayName": row.get("displayName", row["name"]),
                              "created": row.get("created", ""), "hasVerifiedBadge": bool(row.get("hasVerifiedBadge"))}, 600)

    async def avatar(self, uid):
        key = "avatar:" + str(uid)
        cached = self.cached(key)
        if cached is not None:
            return cached
        result = await self.fetch("thumbnails.roblox.com", "/v1/users/avatar-headshot",
                                  params={"userIds": str(uid), "size": "150x150", "format": "Png", "isCircular": "false"})
        rows = result.get("data", [])
        if not rows or rows[0].get("state") != "Completed":
            return None
        url = rows[0].get("imageUrl", "")
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not (parsed.hostname or "").endswith(".rbxcdn.com") or parsed.username:
            return None
        async with self.sem:
            async with self.http.get(url, allow_redirects=False, timeout=ClientTimeout(total=8)) as response:
                if response.status != 200 or response.content_type not in ("image/png", "image/jpeg", "image/webp"):
                    return None
                chunks, total = [], 0
                async for chunk in response.content.iter_chunked(65536):
                    total += len(chunk)
                    if total > 1_000_000:
                        return None
                    chunks.append(chunk)
                raw = b"".join(chunks)
                return self.put(key, (raw, response.content_type), 900)


class RateLimiter:
    def __init__(self):
        self.buckets = OrderedDict()

    def allow(self, key, count=60, period=60):
        ts = time.monotonic()
        bucket = self.buckets.setdefault(key, deque())
        self.buckets.move_to_end(key)
        while bucket and bucket[0] < ts - period:
            bucket.popleft()
        allowed = len(bucket) < count
        if allowed:
            bucket.append(ts)
        while len(self.buckets) > 5000:
            self.buckets.popitem(last=False)
        return allowed


class Service:
    def __init__(self, cfg, db):
        self.cfg, self.db, self.store = cfg, db, Store(cfg, db)
        self.rate, self.tasks, self.ready = RateLimiter(), [], False
        self.http = self.tg = self.roblox = None

    async def enqueue(self, mid, method, payload):
        await self.db.run(lambda tx: tx.enqueue(mid, method, payload))

    async def say(self, uid, text, keyboard=None, mid=None, key_ids=None):
        payload = {"chat_id": uid, "text": text, "parse_mode": "HTML", "link_preview_options": {"is_disabled": True}}
        if key_ids:
            payload["_key_ids"] = key_ids
        if keyboard:
            payload["reply_markup"] = {"inline_keyboard": keyboard}
        await self.enqueue(mid or secrets.token_hex(16), "sendMessage", payload)

    def menu(self, has_access=False):
        buttons = [[{"text": "🎁 Открыть Gifter", "web_app": {"url": self.cfg.public_url}, "style": "primary"}],
                   [{"text": "⭐ Купить ключ", "callback_data": "stars"}, {"text": "🔑 Мои ключи", "callback_data": "keys"}]]
        if has_access:
            buttons.insert(1, [{"text": "⚙️ Настроить панель", "callback_data": "profile", "style": "primary"}])
        if self.cfg.group_url:
            buttons.append([{"text": "💬 Общий чат", "url": self.cfg.group_url}])
        return buttons

    async def welcome(self, uid, event):
        def read(tx):
            tx.execute("UPDATE profile_drafts SET awaiting='' WHERE user_id=?", (uid,))
            return self.store.available_license(tx, uid), self.store.profile(tx, uid)
        license_row, profile = await self.db.run(read)
        if license_row:
            status = ("срок начнётся с первого входа" if license_row["activated_at"] is None else
                      "без срока действия" if license_row["expires_at"] is None else "до " + utc(license_row["expires_at"]))
            text = ("🎁 <b>GIFTER · Ваша панель</b>\n\n"
                    f"🔑 Доступ: {status}\n👤 Ник: <b>{html.escape(profile['nickname'])}</b>\n"
                    f"💎 Демо-баланс: <b>{profile['balance']:,}</b>\n\n"
                    "Нажмите «Настроить панель», измените ник и количество демо-Robux, затем «Сохранить».\n"
                    "<b>DEMO: реальные Robux не отправляются.</b>")
        else:
            text = ("🎁 <b>GIFTER</b>\n\nИнтерфейс, поиск игроков, аватары и анимации.\n"
                    "<b>DEMO: реальные Robux не отправляются.</b>\n\n"
                    "Получите ключ через /stars или у администратора. После этого в /start появятся настройки панели.\n"
                    "Мои ключи: /key · Поддержка: /paysupport")
        if uid in self.cfg.admin_ids:
            text += "\n\n⚙️ Администратор: <code>/give 1h</code> — ключ себе; <code>/give 1h TELEGRAM_ID</code> — пользователю."
        await self.say(uid, text, self.menu(bool(license_row)), event + ":welcome")

    async def give(self, uid, arg, msg, event):
        if uid not in self.cfg.admin_ids:
            await self.say(uid, "Команда /give доступна только администратору из ENV ADMIN_ID.", mid=event + ":give-denied")
            return
        try:
            parts = arg.split()
            if not 1 <= len(parts) <= 2:
                raise ValueError("Формат: /give 1m|1h|1d|1w|lifetime [TELEGRAM_ID]. Без ID — ключ себе; ответом на сообщение человека — ему.")
            reply = msg.get("reply_to_message", {}).get("from", {})
            if len(parts) == 2:
                if not re.fullmatch(r"[1-9][0-9]{0,15}", parts[1]):
                    raise ValueError("Укажите числовой Telegram ID, без @username.")
                target = int(parts[1])
            elif reply:
                if reply.get("is_bot") or msg.get("reply_to_message", {}).get("sender_chat"):
                    raise ValueError("Ответьте на сообщение человека или укажите его Telegram ID.")
                target = reply.get("id")
            else:
                target = uid
            row = await self.db.run(lambda tx: self.store.grant(tx, uid, target, parts[0], event))
        except (ValueError, PermissionError) as exc:
            await self.say(uid, html.escape(str(exc)), mid=event + ":give-error")
            return
        text = (f"🔑 <b>Доступ выдан · {html.escape(plan_label(row['plan']))}</b>\n\n"
                f"Пользователь: <code>{target}</code>\nКлюч:\n<code>[[key:{row['id']}]]</code>\n\n"
                "Срок начнётся с первого входа и не сбрасывается при повторном входе.\n"
                "Настройки ника и демо-баланса: /start → «Настроить панель».\n"
                "Ключ открывает DEMO-интерфейс; реальные Robux не переводятся.")
        await self.say(target, text, self.menu(True), event + ":give-recipient", [row["id"]])
        if target != uid:
            await self.say(uid, text + "\n\nЕсли пользователь ещё не запускал бота, попросите его отправить /start и передайте ключ лично.",
                           mid=event + ":give-admin", key_ids=[row["id"]])

    async def profile_card(self, uid, draft, event):
        did = draft["draft_id"]
        keyboard = [[{"text": "💎 Демо-баланс", "callback_data": "profile:balance:" + did},
                     {"text": "👤 Ник профиля", "callback_data": "profile:nickname:" + did}],
                    [{"text": "💾 Сохранить", "callback_data": "profile:save:" + did, "style": "success"},
                     {"text": "Отмена", "callback_data": "profile:cancel:" + did}]]
        await self.say(uid, "⚙️ <b>Настройки вашей панели</b>\n\n"
                       f"👤 Ник: <b>{html.escape(draft['nickname'])}</b>\n"
                       f"💎 Демо-баланс: <b>{draft['balance']:,}</b>\n\n"
                       "Выберите поле и пришлите новое значение сообщением.\n"
                       "Изменения применятся только после «Сохранить».\n"
                       "Это отображение внутри DEMO; аккаунт Roblox не изменяется.", keyboard, event + ":profile-card")

    async def profile_action(self, uid, data, event):
        try:
            if data == "profile":
                draft = await self.db.run(lambda tx: self.store.open_profile(tx, uid, event))
                await self.profile_card(uid, draft, event)
                return
            _, action, did = data.split(":", 2)
            if action in ("balance", "nickname"):
                await self.db.run(lambda tx: self.store.await_profile_field(tx, uid, did, action))
                prompt = ("💎 Введите демо-баланс от 0 до 9 999 999 999, например <code>500000</code>." if action == "balance" else
                          "👤 Введите ник для верхней панели и профиля слева: от 1 до 32 видимых символов.")
                await self.say(uid, prompt + "\n\nПосле ввода нажмите «Сохранить». Отмена: /cancel.", mid=event + ":profile-prompt")
            elif action == "save":
                profile = await self.db.run(lambda tx: self.store.save_profile(tx, uid, did, event))
                await self.say(uid, "✅ <b>Настройки сохранены</b>\n\n"
                               f"👤 {html.escape(profile['nickname'])}\n💎 {profile['balance']:,} демо-Robux\n\n"
                               "Откройте панель: новые значения загрузятся автоматически.", self.menu(True), event + ":profile-saved")
            elif action == "cancel":
                await self.db.run(lambda tx: tx.execute("DELETE FROM profile_drafts WHERE user_id=? AND draft_id=?", (uid, did)))
                await self.say(uid, "Изменения отменены. Открыть настройки заново: /settings.", mid=event + ":profile-cancel")
        except ValueError as exc:
            await self.say(uid, html.escape(str(exc)), mid=event + ":profile-error")

    async def stars(self, uid, event):
        keys = []
        items = list(PLANS.items())
        for i in range(0, len(items), 2):
            row = []
            for pid, plan in items[i:i + 2]:
                btn = {"text": f"{plan['label']} · {plan['stars']} ⭐", "callback_data": "buy:" + pid,
                       "style": "success" if pid == "forever" else "primary"}
                if self.cfg.star_emoji:
                    btn["icon_custom_emoji_id"] = self.cfg.star_emoji
                row.append(btn)
            keys.append(row)
        keys.append([{"text": "🔑 Мои ключи", "callback_data": "keys"}, {"text": "📄 Условия", "callback_data": "terms"}])
        caption = ("<b>GIFTER · Выберите свой доступ</b>\n\n"
                   "⭐ Одна оплата — один ключ\n⏱ Срок с первой активации\n♾ Навсегда — без срока действия\n\n"
                   "<b>Вы покупаете доступ к визуальному DEMO.</b>\n"
                   "Ключ не выдаёт Robux и не выполняет реальные переводы.\n"
                   "Поддержка и возвраты: /paysupport · Условия: /terms")
        await self.enqueue(event + ":stars", "sendPhoto", {"chat_id": uid, "caption": caption,
                         "parse_mode": "HTML", "reply_markup": {"inline_keyboard": keys}, "_embedded_banner": True})

    async def keys(self, uid, event):
        rows = await self.db.run(lambda tx: tx.all("SELECT o.id,o.plan,l.* FROM licenses l JOIN orders o ON o.id=l.order_id WHERE l.owner_id=? ORDER BY o.paid_at DESC LIMIT 12", (uid,)))
        lines = ["🔑 <b>Ваши ключи</b>"]
        for row in rows:
            if row["revoked"]:
                status = "отозван после возврата"
            elif row["activated_at"] is None:
                status = "ожидает активации"
            elif row["duration"] is None:
                status = "без срока действия"
            else:
                status = ("истёк " if row["expires_at"] <= now() else "до ") + utc(row["expires_at"])
            lines.append(f"\n<b>{html.escape(plan_label(row['plan']))}</b> · {status}\n<code>[[key:{row['order_id']}]]</code>")
        if not rows:
            lines.append("\nКлючей пока нет. Выберите тариф в /stars.")
        await self.say(uid, "\n".join(lines), self.menu(), event + ":keys", [r["order_id"] for r in rows])

    async def invoice(self, uid, pid, event):
        if pid not in PLANS:
            return
        # A repeated callback update must not create another order/invoice.
        def create(tx):
            existing = tx.one("SELECT value FROM settings WHERE key=?", ("invoice:" + event,))
            if existing:
                return
            order = self.store.order(tx, uid, pid)
            tx.execute("INSERT INTO settings(key,value) VALUES(?,?)", ("invoice:" + event, order["id"]))
            label = PLANS[pid]["label"]
            tx.enqueue(event + ":invoice", "sendInvoice", {"chat_id": uid, "title": f"Gifter DEMO · {label}",
                "description": "Доступ к визуальному DEMO гифтера. Robux не переводятся и не входят в покупку. Срок с первой активации. Условия: /terms. Возвраты: /paysupport.",
                "payload": order["id"], "provider_token": "", "currency": "XTR",
                "prices": [{"label": label, "amount": order["stars"]}], "start_parameter": "order_" + order["id"],
                "reply_markup": {"inline_keyboard": [[{"text": f"Оплатить {order['stars']} ⭐", "pay": True, "style": "success"}]]}})
        await self.db.run(create)

    async def process(self, update):
        event = "u" + str(update["update_id"])
        callback = update.get("callback_query")
        if callback:
            uid, data = callback.get("from", {}).get("id"), callback.get("data", "")
            message = callback.get("message", {})
            if message.get("chat", {}).get("type") != "private" or message.get("chat", {}).get("id") != uid:
                return
            try:
                await self.tg.call("answerCallbackQuery", {"callback_query_id": callback["id"]})
            except TelegramError as exc:
                if exc.code != 400:
                    raise
            if data == "stars":
                await self.stars(uid, event)
            elif data == "keys":
                await self.keys(uid, event)
            elif data == "terms":
                await self.say(uid, TERMS, mid=event + ":terms")
            elif data == "profile" or data.startswith("profile:"):
                await self.profile_action(uid, data, event)
            elif data.startswith("buy:"):
                await self.invoice(uid, data[4:], event)
            elif data.startswith("refund:") and uid in self.cfg.admin_ids:
                oid = data[7:]
                def queue_refund(tx):
                    row = tx.one("SELECT * FROM orders WHERE id=?", (oid,), lock=True)
                    if not row or row["status"] != "paid":
                        return False
                    tx.enqueue("refund:" + oid, "refundStarPayment", {"user_id": row["user_id"], "telegram_payment_charge_id": row["charge_id"]})
                    return True
                ok = await self.db.run(queue_refund)
                await self.say(uid, "Возврат поставлен в обработку." if ok else "Оплаченный заказ не найден или уже возвращён.", mid=event + ":refund")
            return
        msg = update.get("message") or update.get("edited_message")
        if not msg:
            return
        uid, chat = msg.get("from", {}).get("id"), msg.get("chat", {})
        if not uid:
            return
        if chat.get("type") != "private":
            if chat.get("id") == self.cfg.group_id and uid != self.tg.id:
                parts = msg.get("text", "").strip().split(maxsplit=1)
                command = parts[0].lower() if parts else ""
                if (not update.get("edited_message") and not msg.get("sender_chat") and
                        not msg.get("from", {}).get("is_bot") and uid in self.cfg.admin_ids and
                        command in ("/give", "/give@" + (self.tg.username or "").lower())):
                    await self.give(uid, parts[1] if len(parts) > 1 else "", msg, event)
                locked = await self.db.run(lambda tx: tx.one("SELECT value FROM settings WHERE key='chat_locked'"))
                if locked and locked["value"] == "1":
                    await self.enqueue(event + ":delete", "deleteMessage", {"chat_id": chat["id"], "message_id": msg["message_id"]})
            return
        if "successful_payment" in msg:
            await self.db.run(lambda tx: self.store.paid(tx, uid, msg["successful_payment"]))
            return
        if "refunded_payment" in msg:
            await self.db.run(lambda tx: self.store.refunded(tx, msg["refunded_payment"]["telegram_payment_charge_id"]))
            return
        if update.get("edited_message"):
            return
        text = msg.get("text", "").strip()
        command, _, arg = text.partition(" ")
        command = command.split("@")[0].lower()
        if not text.startswith("/") and text:
            try:
                draft = await self.db.run(lambda tx: self.store.edit_profile(tx, uid, text, event))
                if draft:
                    await self.profile_card(uid, draft, event)
                    return
            except ValueError as exc:
                await self.say(uid, html.escape(str(exc)), mid=event + ":profile-input-error")
                return
        if command not in ("/paysupport", "/cancel") and not text.startswith("/"):
            pending = await self.db.run(lambda tx: tx.one("SELECT * FROM support_pending WHERE user_id=?", (uid,)))
            if pending and pending["expires_at"] > now():
                command, arg = "/paysupport", text
        if command == "/start" and arg.strip() == "stars":
            await self.stars(uid, event)
        elif command in ("/start", "/app"):
            await self.welcome(uid, event)
        elif command == "/give":
            await self.give(uid, arg, msg, event)
        elif command == "/settings":
            await self.profile_action(uid, "profile", event)
        elif command == "/stars":
            await self.stars(uid, event)
        elif command in ("/key", "/status"):
            await self.keys(uid, event)
        elif command == "/terms":
            await self.say(uid, TERMS, mid=event + ":terms")
        elif command == "/privacy":
            await self.say(uid, PRIVACY, mid=event + ":privacy")
        elif command == "/cancel":
            await self.db.run(lambda tx: (tx.execute("DELETE FROM support_pending WHERE user_id=?", (uid,)),
                                         tx.execute("DELETE FROM profile_drafts WHERE user_id=?", (uid,))))
            await self.say(uid, "Ввод отменён. Несохранённые настройки удалены. Главное меню: /start.", mid=event + ":cancel")
        elif command == "/paysupport":
            await self.db.run(lambda tx: tx.execute("UPDATE profile_drafts SET awaiting='' WHERE user_id=?", (uid,)))
            if not arg.strip():
                await self.db.run(lambda tx: tx.execute("INSERT INTO support_pending(user_id,expires_at) VALUES(?,?) ON CONFLICT(user_id) DO UPDATE SET expires_at=excluded.expires_at", (uid, now() + 900)))
                extra = f"\nТакже: @{self.cfg.support}" if self.cfg.support else ""
                await self.say(uid, "Опишите проблему следующим текстовым сообщением, укажите ID заказа из чека. Вопрос будет передан владельцу.\nОтмена: /cancel." + extra, mid=event + ":support-prompt")
            else:
                for owner in self.cfg.admin_ids:
                    await self.say(owner, f"🛟 <b>Оплата / поддержка</b>\nПользователь: <a href=\"tg://user?id={uid}\">{uid}</a>\n\n{html.escape(arg[:2500])}", mid=event + ":support:" + str(owner))
                await self.db.run(lambda tx: tx.execute("DELETE FROM support_pending WHERE user_id=?", (uid,)))
                await self.say(uid, "Обращение передано владельцу. Сохраните чек Telegram до решения вопроса.", mid=event + ":support-sent")
        elif command == "/find":
            try:
                rows = await self.roblox.search(arg)
                result = "\n\n".join(f"<b>{html.escape(x['displayName'])}</b> · @{html.escape(x['name'])}\nhttps://www.roblox.com/users/{x['id']}/profile" for x in rows[:5])
                await self.say(uid, result or "Ничего не найдено.", mid=event + ":find")
            except (ValueError, asyncio.TimeoutError):
                await self.say(uid, "Поиск не удался. Пример: /find Roblox. Попробуйте точный username ещё раз позже.", mid=event + ":find-error")
        elif command == "/lockchat" and uid in self.cfg.admin_ids:
            await self.lockchat(uid, event)
        elif command == "/admin" and uid in self.cfg.admin_ids:
            data = await self.db.run(lambda tx: {"sales": tx.one("SELECT COUNT(*) AS n,COALESCE(SUM(stars),0) AS total FROM orders WHERE status='paid'"),
                "incidents": tx.one("SELECT COUNT(*) AS n FROM payment_incidents"),
                "failed": tx.one("SELECT COUNT(*) AS n FROM outbox WHERE status='failed'")})
            await self.say(uid, f"⚙️ <b>Gifter</b>\nОплачено: {data['sales']['n']}\nStars: {data['sales']['total']}\n"
                           f"Платежей для разбора: {data['incidents']['n']}\nОшибок доставки: {data['failed']['n']}\n\n"
                           "/give 1h [TELEGRAM_ID] — выдать ключ (1m, 1h, 1d, 1w, lifetime)\n"
                           "/refund ORDER_ID — возврат с подтверждением\n/lockchat — закрыть общий чат для сообщений участников", mid=event + ":admin")
        elif command == "/refund" and uid in self.cfg.admin_ids:
            row = await self.db.run(lambda tx: tx.one("SELECT * FROM orders WHERE id=? AND status='paid'", (arg.strip(),)))
            if row:
                await self.say(uid, f"Вернуть {row['stars']} ⭐ покупателю {row['user_id']}?\nКлюч этого заказа будет отозван.",
                    [[{"text": "↩️ Подтвердить возврат", "style": "danger", "callback_data": "refund:" + row["id"]}]], event + ":refund-confirm")
            else:
                await self.say(uid, "Оплаченный заказ не найден. Формат: /refund ORDER_ID", mid=event + ":refund-missing")
        else:
            await self.say(uid, "Открыть интерфейс: /app\nКупить доступ: /stars\nМои ключи: /key\nПоддержка оплаты: /paysupport", mid=event + ":help")

    async def lockchat(self, owner, event):
        if not self.cfg.group_id:
            await self.say(owner, "Сначала задайте GROUP_CHAT_ID в Render.", mid=event + ":lock-no-id")
            return
        chat = await self.tg.call("getChat", {"chat_id": self.cfg.group_id})
        if chat.get("type") != "supergroup":
            await self.say(owner, "Для /lockchat нужна супергруппа. В канале настройте права публикации администраторов вручную.", mid=event + ":lock-type")
            return
        member = await self.tg.call("getChatMember", {"chat_id": self.cfg.group_id, "user_id": self.tg.id})
        if not member.get("can_restrict_members") or not member.get("can_delete_messages"):
            await self.say(owner, "Дайте боту права администратора: ограничивать участников и удалять сообщения.", mid=event + ":lock-rights")
            return
        fields = ["can_send_messages", "can_send_audios", "can_send_documents", "can_send_photos", "can_send_videos",
                  "can_send_video_notes", "can_send_voice_notes", "can_send_polls", "can_send_other_messages",
                  "can_add_web_page_previews", "can_change_info", "can_invite_users", "can_pin_messages", "can_manage_topics"]
        await self.tg.call("setChatPermissions", {"chat_id": self.cfg.group_id, "permissions": {k: False for k in fields}, "use_independent_chat_permissions": True})
        await self.db.run(lambda tx: tx.execute("INSERT INTO settings(key,value) VALUES('chat_locked','1') ON CONFLICT(key) DO UPDATE SET value='1'"))
        await self.say(owner, "Чат закрыт для сообщений обычных участников. Сообщения людей бот будет удалять. Администраторы и владелец сохраняют права Telegram.", mid=event + ":locked")

    async def claim(self, table):
        assert table in ("inbox", "outbox")
        def take(tx):
            row = tx.one(f"SELECT * FROM {table} WHERE status IN ('pending','working') AND lease<=? ORDER BY lease LIMIT 1", (now(),), lock=True)
            if row:
                tx.execute(f"UPDATE {table} SET status='working',lease=?,attempts=attempts+1 WHERE id=?", (now() + 90, row["id"]))
            return row
        return await self.db.run(take)

    async def worker(self, table):
        while True:
            row = None
            try:
                row = await self.claim(table)
                if not row:
                    await asyncio.sleep(0.4)
                    continue
                payload = json.loads(row["payload"])
                if table == "inbox":
                    await self.process(payload)
                else:
                    banner = payload.pop("_embedded_banner", False)
                    for oid in payload.pop("_key_ids", []):
                        payload["text"] = payload["text"].replace("[[key:" + oid + "]]", key_for(oid, self.cfg.secret))
                    try:
                        await self.tg.call(row["method"], payload, base64.b64decode(BANNER_PNG) if banner else None)
                    except TelegramError as exc:
                        if row["method"] == "refundStarPayment" and "CHARGE_ALREADY_REFUNDED" in exc.description:
                            pass
                        elif row["method"] == "deleteMessage" and exc.code == 400 and "not found" in exc.description.lower():
                            pass
                        else:
                            raise
                    if row["method"] == "refundStarPayment":
                        await self.db.run(lambda tx: self.store.refunded(tx, payload["telegram_payment_charge_id"]))
                await self.db.run(lambda tx: tx.execute(f"UPDATE {table} SET status='done',lease=? WHERE id=?", (now(), row["id"])))
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                LOG.warning("%s delivery failed: %s", table, type(exc).__name__)
                if row:
                    fatal = isinstance(exc, TelegramError) and exc.code in (400, 403)
                    delay = max(min(300, 2 ** min(row["attempts"] + 1, 8)), getattr(exc, "retry_after", 0))
                    try:
                        await self.db.run(lambda tx: tx.execute(f"UPDATE {table} SET status=?,lease=? WHERE id=?",
                            ("failed" if fatal else "pending", now() + delay, row["id"])))
                    except Exception:
                        LOG.error("Could not release queue lease; will retry after lease expires")
                await asyncio.sleep(2)

    async def register(self):
        while True:
            try:
                me = await self.tg.call("getMe", {})
                self.tg.username, self.tg.id = me["username"], me["id"]
                await self.tg.call("setWebhook", {"url": self.cfg.public_url + "/telegram/webhook",
                    "secret_token": self.cfg.webhook_secret, "max_connections": 10,
                    "allowed_updates": ["message", "edited_message", "callback_query", "pre_checkout_query"],
                    "drop_pending_updates": False})
                commands = [("start", "Главное меню"), ("stars", "Купить доступ за Stars"), ("app", "Открыть Gifter"),
                            ("key", "Мои ключи"), ("settings", "Ник и демо-баланс панели"), ("status", "Срок доступа"), ("find", "Найти игрока Roblox"),
                            ("paysupport", "Помощь с оплатой и возвратом"), ("terms", "Условия доступа"), ("privacy", "Данные и приватность")]
                await self.tg.call("setMyCommands", {"commands": [{"command": a, "description": b} for a, b in commands]})
                await self.tg.call("setChatMenuButton", {"menu_button": {"type": "web_app", "text": "Gifter", "web_app": {"url": self.cfg.public_url}}})
                for admin in self.cfg.admin_ids:
                    try:
                        await self.tg.call("setMyCommands", {"scope": {"type": "chat", "chat_id": admin},
                            "commands": [{"command": a, "description": b} for a, b in commands + [("give", "Выдать ключ: /give 1h [ID]"), ("admin", "Управление ботом")]]})
                    except TelegramError:
                        LOG.info("Admin command menu will be available after the admin starts the bot")
                self.ready = True
                LOG.info("Telegram webhook ready")
                return
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                LOG.warning("Bot registration failed (%s); retry in 10s", type(exc).__name__)
                await asyncio.sleep(10)


TERMS = ("📄 <b>Условия GIFTER</b>\n\nВы покупаете доступ к демонстрационному интерфейсу, а не Robux. "
         "Сервис не выполняет реальные переводы и не связан с Roblox Corporation. Поиск использует публичные данные Roblox.\n\n"
         "Один платёж — отдельный ключ. Срок начинается при первой активации; повторный вход не перезапускает срок. "
         "Тариф «Навсегда» не имеет календарного срока, но доступ зависит от работы сервиса. "
         "Повторная покупка не продлевает существующий ключ. Ключ следует хранить как пароль.\n\n"
         "Цены: 1 час — 5 ⭐; 2 часа — 15 ⭐; 1 день — 30 ⭐; 2 дня — 50 ⭐; 5 дней — 100 ⭐; навсегда — 400 ⭐.\n\n"
         "Для проблем с оплатой или запроса возврата: /paysupport. После возврата соответствующий ключ отзывается. "
         "Решение по обращению принимает владелец сервиса. Применимые права покупателя сохраняются.\n\nДанные: /privacy")
PRIVACY = ("🔒 <b>Данные GIFTER</b>\n\nСохраняем Telegram ID, заказ, сумму Stars, идентификатор оплаты, "
           "хеш ключа, время активации, сессии, заданные ник/демо-баланс и историю демонстраций. Обращения /paysupport получает владелец. "
           "В общий чат попадает только тариф и короткий номер покупки — без ключа и Telegram ID. "
           "Поисковый запрос отправляется Roblox для поиска публичного профиля. "
           "Пароли, cookie и платёжные карты Roblox не нужны. В браузере хранится HttpOnly-cookie сессии и выбранная тема. "
           "Входящие сообщения хранятся в очереди обработки до 7 дней; чеки и история — пока владелец не удалит их. "
           "Удаление данных и вопросы: /paysupport.")


FALLBACK_AVATAR = b'''<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150"><rect width="150" height="150" rx="75" fill="#30323b"/><path d="M35 141v-20c0-30 80-30 80 0v20" fill="#727989"/><rect x="48" y="32" width="54" height="60" rx="17" fill="#aeb6c7"/><path d="M62 60v4m26-4v4m-23 12q10 8 20 0" stroke="#30323b" stroke-width="5" stroke-linecap="round" fill="none"/></svg>'''


def js_safe(value):
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


async def json_body(request):
    if request.content_type != "application/json":
        raise ValueError("Ожидается JSON")
    data = await request.json()
    if not isinstance(data, dict):
        raise ValueError("Ожидается объект JSON")
    return data


@web.middleware
async def middleware(request, handler):
    svc = request.app["svc"]
    cfg = svc.cfg
    nonce = secrets.token_urlsafe(16)
    request["nonce"] = nonce
    try:
        if request.path.startswith("/api/"):
            ip = request.remote or "unknown"
            if not svc.rate.allow(("http", ip), 240):
                raise web.HTTPTooManyRequests(text="Слишком много запросов", headers={"Retry-After": "60"})
            if request.method == "POST":
                allowed = cfg.public_url if not cfg.preview else "http://" + request.host
                if request.headers.get("Origin") != allowed:
                    raise web.HTTPForbidden(text="Origin rejected")
                if request.path in ("/api/activate", "/api/telegram") and not svc.rate.allow(("login", ip), 20):
                    raise web.HTTPTooManyRequests(text="Слишком много попыток входа", headers={"Retry-After": "60"})
        response = await handler(request)
    except web.HTTPException as exc:
        response = web.json_response({"error": exc.text or exc.reason}, status=exc.status, headers={k: v for k, v in exc.headers.items() if k.lower() == "retry-after"})
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        response = web.json_response({"error": str(exc) if isinstance(exc, ValueError) else "Неверные данные запроса"}, status=400)
    except PermissionError:
        response = web.json_response({"error": "Сессия истекла. Войдите по ключу."}, status=401)
    except asyncio.TimeoutError:
        response = web.json_response({"error": "Сервис не ответил вовремя. Повторите запрос."}, status=503)
    except Exception as exc:
        LOG.error("Request failed: %s", type(exc).__name__)
        response = web.json_response({"error": "Временная ошибка сервера. Повторите запрос позже."}, status=503)
    response.headers.update({
        "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
        "Content-Security-Policy": f"default-src 'self'; script-src 'self' 'nonce-{nonce}' https://telegram.org; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'self' https://web.telegram.org https://*.telegram.org",
    })
    if request.path.startswith("/api/") or request.path == "/":
        response.headers["Cache-Control"] = "no-store"
    if not cfg.preview:
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response


async def auth(request):
    svc = request.app["svc"]
    row = await svc.db.run(lambda tx: svc.store.session(tx, request_token(request)))
    if not row:
        raise PermissionError()
    return row


def request_token(request):
    # Memory-only bearer fallback supports Telegram Web with third-party cookies blocked.
    header = request.headers.get("Authorization", "")
    return header[7:] if header.startswith("Bearer ") else request.cookies.get("gifter_session", "")


def session_response(cfg, token, expires):
    response = web.json_response({"ok": True, "session_token": token})
    response.set_cookie("gifter_session", token, httponly=True, secure=not cfg.preview,
                        samesite="Strict", max_age=max(0, expires - now()), path="/")
    return response


async def index(request):
    return web.Response(text=HTML.replace("__NONCE__", request["nonce"]), content_type="text/html")


async def config_api(request):
    svc = request.app["svc"]
    return web.json_response({"preview": svc.cfg.preview, "bot": svc.tg.username,
        "plans": PLANS, "group_url": svc.cfg.group_url,
        "support": svc.cfg.support, "demo_only": True})


async def health(request):
    svc = request.app["svc"]
    await svc.db.run(lambda tx: tx.one("SELECT 1 AS ok"))
    return web.json_response({"status": "ok", "telegram": "disabled-preview" if svc.cfg.preview else ("ready" if svc.ready else "connecting")})


async def activate_api(request):
    svc, body = request.app["svc"], await json_body(request)
    key = body.get("key", "")
    if not isinstance(key, str) or len(key) > 100:
        raise ValueError("Неверный формат ключа")
    token, expires = await svc.db.run(lambda tx: svc.store.activate(tx, key))
    return session_response(svc.cfg, token, expires)


async def telegram_auth_api(request):
    svc, body = request.app["svc"], await json_body(request)
    if svc.cfg.preview:
        raise ValueError("Telegram выключен в preview")
    user = verify_init_data(body.get("init_data", ""), svc.cfg.token)
    def login(tx):
        row = svc.store.available_license(tx, user["id"])
        if not row:
            raise ValueError("У вас пока нет активного ключа. Выберите тариф в /stars.")
        key = key_for(row["order_id"], svc.cfg.secret)
        return svc.store.activate(tx, key, required_uid=user["id"])
    token, expires = await svc.db.run(login)
    return session_response(svc.cfg, token, expires)


async def logout_api(request):
    svc = request.app["svc"]
    token = request_token(request)
    await svc.db.run(lambda tx: tx.execute("DELETE FROM sessions WHERE token_hash=?", (digest(token),)))
    response = web.json_response({"ok": True})
    response.del_cookie("gifter_session", path="/")
    return response


async def me_api(request):
    svc = request.app["svc"]
    def read(tx):
        row = svc.store.session(tx, request_token(request))
        if not row:
            raise PermissionError()
        order = tx.one("SELECT plan FROM orders WHERE id=?", (row["order_id"],))
        return {**svc.store.profile(tx, row["owner_id"]), "expires_at": row["expires_at"],
                "session_expires_at": row["session_expiry"], "server_time": time.time(),
                "plan": order["plan"], "demo": True}
    return web.json_response(await svc.db.run(read))


async def search_api(request):
    await auth(request)
    svc = request.app["svc"]
    if not svc.rate.allow(("search", digest(request_token(request))), 30):
        raise web.HTTPTooManyRequests(text="Поиск слишком частый. Подождите минуту.")
    return web.json_response({"users": await svc.roblox.search(request.query.get("q", ""))})


async def user_api(request):
    await auth(request)
    return web.json_response(await request.app["svc"].roblox.user(int(request.match_info["uid"])))


async def avatar_api(request):
    await auth(request)
    uid = int(request.match_info["uid"])
    if not 1 <= uid <= 10**14:
        raise ValueError("Неверный ID")
    try:
        asset = await request.app["svc"].roblox.avatar(uid)
    except Exception:
        asset = None
    if asset:
        return web.Response(body=asset[0], content_type=asset[1])
    return web.Response(body=FALLBACK_AVATAR, content_type="image/svg+xml")


async def history_api(request):
    row = await auth(request)
    rows = await request.app["svc"].db.run(lambda tx: tx.all("SELECT id,recipient_id,recipient_name,amount,created_at FROM gifts WHERE owner_id=? ORDER BY created_at DESC LIMIT 30", (row["owner_id"],)))
    return web.json_response({"gifts": rows, "demo": True})


async def gift_api(request):
    row = await auth(request)
    svc, body = request.app["svc"], await json_body(request)
    amount, rid, request_id = body.get("amount"), body.get("recipient_id"), body.get("request_id")
    if type(rid) is not int or type(amount) is not int or not 1 <= rid <= 10**14:
        raise ValueError("Неверные ID или сумма")
    if not isinstance(request_id, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{16,80}", request_id):
        raise ValueError("Неверный ID операции")
    existing = await svc.db.run(lambda tx: tx.one("SELECT * FROM gifts WHERE owner_id=? AND request_id=?", (row["owner_id"], request_id)))
    # Retry must also work when Roblox is temporarily unavailable.
    player = {"name": existing["recipient_name"]} if existing else await svc.roblox.user(rid)
    result = await svc.db.run(lambda tx: svc.store.gift(tx, request_token(request), rid, player["name"], amount, request_id))
    return web.json_response({"gift": result, "demo": True, "robux_transferred": False})


async def webhook(request):
    svc = request.app["svc"]
    if svc.cfg.preview or not hmac.compare_digest(request.headers.get("X-Telegram-Bot-Api-Secret-Token", ""), svc.cfg.webhook_secret):
        raise web.HTTPForbidden(text="Invalid webhook secret")
    update = await json_body(request)
    if type(update.get("update_id")) is not int:
        raise ValueError("Invalid update")
    if "pre_checkout_query" in update:
        query = update["pre_checkout_query"]
        error = await svc.db.run(lambda tx: svc.store.precheck(tx, query))
        payload = {"method": "answerPreCheckoutQuery", "pre_checkout_query_id": query["id"], "ok": error is None}
        if error:
            payload["error_message"] = error
        # Inline webhook reply avoids an extra network hop in the 10s deadline.
        return web.json_response(payload)
    await svc.db.run(lambda tx: tx.execute("INSERT INTO inbox(id,payload) VALUES(?,?) ON CONFLICT(id) DO NOTHING",
                                           (update["update_id"], json.dumps(update, ensure_ascii=False))))
    return web.json_response({"ok": True})


async def cleanup_data(svc):
    while True:
        await asyncio.sleep(3600)
        try:
            def clean(tx):
                tx.execute("DELETE FROM sessions WHERE expires_at<?", (now(),))
                tx.execute("DELETE FROM support_pending WHERE expires_at<?", (now(),))
                tx.execute("DELETE FROM profile_drafts WHERE expires_at<=?", (now(),))
                # Retain IDs for durable deduplication while removing message bodies.
                tx.execute("UPDATE inbox SET payload='{}' WHERE status='done' AND lease<? AND payload<>'{}'", (now() - 604800,))
                tx.execute("UPDATE outbox SET payload='{}' WHERE status='done' AND lease<? AND payload<>'{}'", (now() - 604800,))
            await svc.db.run(clean)
        except Exception as exc:
            LOG.warning("Cleanup failed: %s", type(exc).__name__)


async def lifecycle(app):
    svc = app["svc"]
    svc.http = ClientSession(timeout=ClientTimeout(total=15), headers={"User-Agent": "GifterDemo/1.0"})
    svc.tg, svc.roblox = Telegram(svc.cfg, svc.http), Roblox(svc.http)
    if not svc.cfg.preview:
        svc.tasks = [asyncio.create_task(svc.register()), asyncio.create_task(svc.worker("inbox")),
                     asyncio.create_task(svc.worker("outbox")), asyncio.create_task(cleanup_data(svc))]
    yield
    for task in svc.tasks:
        task.cancel()
    await asyncio.gather(*svc.tasks, return_exceptions=True)
    await svc.http.close()
    svc.db.close()


def make_app(cfg):
    cfg.validate()
    db = Database(cfg)
    svc = Service(cfg, db)
    if cfg.preview:
        def seed(tx):
            order = svc.store.order(tx, 1, "forever")
            tx.execute("UPDATE orders SET status='paid',paid_at=? WHERE id=?", (now(), order["id"]))
            tx.execute("INSERT INTO licenses(key_hash,order_id,owner_id,duration) VALUES(?,?,1,NULL)", (digest("DEMO-LOCAL"), order["id"]))
            tx.execute("INSERT INTO wallets(owner_id,balance) VALUES(1,?) ON CONFLICT DO NOTHING", (DEMO_BALANCE,))
        db.run_sync(seed)
    app = web.Application(middlewares=[middleware], client_max_size=65536)
    app["svc"] = svc
    app.cleanup_ctx.append(lifecycle)
    app.add_routes([
        web.get("/", index), web.get("/healthz", health), web.get("/api/config", config_api),
        web.post("/api/activate", activate_api), web.post("/api/telegram", telegram_auth_api),
        web.post("/api/logout", logout_api), web.get("/api/me", me_api), web.get("/api/users", search_api),
        web.get("/api/user/{uid:\\d+}", user_api), web.get("/api/avatar/{uid:\\d+}", avatar_api),
        web.get("/api/history", history_api), web.post("/api/demo-gifts", gift_api),
        web.post("/telegram/webhook", webhook),
        web.get("/favicon.svg", lambda r: web.Response(text=FAVICON, content_type="image/svg+xml")),
    ])
    return app


FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#335fff"/><path d="M15 28h34v24H15zm-3-10h40v12H12zM32 18v34m0-34c-16 0-18-14-9-13 8 1 9 13 9 13s1-12 9-13c9-1 7 13-9 13" fill="none" stroke="white" stroke-width="4" stroke-linejoin="round"/></svg>'

# Embedded banner is generated artwork, not a screenshot. Filled in below.
BANNER_PNG = "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pzsJLnA/evToggWGTvfo6OjvvvvGchvOdu3aPf/8cyYVvv7624C/z8zMDBj7nqu77x4eEmJ4C8qWLdO3bx+j0vXr1wvvqw8//MhkScDDDz/kPgS//oaHZucA0LPHDb179zI64Mknn87LRLRq1eqvvvrGqOaoF5+3mUfS35914u0T6pAIUoeuIx56AjzQUehuR6G8NY7xKSQYOn78+LdMMideddVVU6b8Uq9eXaMKN9988zfffBUREWFUYcuWrb///rtR6bJly42KGjRoMGrUiwGLYmJiPv7442LFDBewLl++XHhH/fPPP5MnTzYq7dKlc7169dy9lX/8scp8cy6tVLp0qddff9Wo9OdfJheK43rttbH79x8IWLlEieJvvTnOaucmXJkqpjXB47ELAe5ibdDr0+XqslRnW6XKdLcjtaNQLg5BQpzujJsxBQW479ixY+LE700q1K9ff+7cuR98MKFr165VqlSJjIyMjY2tU+fKYcPunD171ltvjTfZYzU7O/v5518wmRhMnDjRxI19993DZ82a2bdvn4oVK0ZERMTExFxxxRXDht25dOni1q1bGR114MCBxYuXyOirDz74yCiyiBDy8MMPun43ZTvdu3TpfOzYUdP/juT/b+NGwywQb7z+WqlSpYzmSC++OLrQW3rx4sURI0ZmZ2cHPKR9+7a33joUB009oFnAAUoD3PlPRLgNFRQno+yGEpe7HfkbhdL8K0JcOXdYkHT86NEvt23bpmbNmkYVwsPD+vXr269fX9aWP/jgQ/PA6xMnTk6dOm3QoIFGFZo2bdK06QdMJ/3ss89NAvd5dODAgdmz5/TqFXjPzp49e44dO948O75sbdmydc6c3264obvmb3q/fn1NjHzs8aeSk5OLLr3cuHHTJ5989sAD9wU86oXnn1myZOnhw0d1AluZrREIliv1zDzG1U8d0cNydLeLU/fB7/kSOe4bJKCRj3/2J4/99qOGSTDZ9k4qUNvwUJZtlVg2YwoKjzsApKWl3Xrr7UlJSYKfv9/mjh//pmW1cePGCzz15s1bJk36UV5fTZhgOIsIDQ198MEHXL+bY8eOM3JLa6JyZcuOeWW0UekPP/xo8geT8ePf3r17T8CimJiYt98ebxUw4wU/hTdO6VGXp7IAdw/GyRC7lmvsbveJJ7774Pf8Su0ob956Td/HoicICZ5n5cCBAwMG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"

HTML = r'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="color-scheme" content="dark light"><meta name="theme-color" content="#111216">
<meta name="description" content="Gifter — a visual UI demo with public Roblox profile search. No real Robux transfers.">
<title>Gifter · Interface Demo</title><link rel="icon" href="/favicon.svg">
<style>
:root{--bg:#111215;--nav:#191a1f;--panel:#1b1c22;--card:#282a33;--hover:#30333e;--border:#30323b;--text:#f7f7f8;--muted:#b5b7c0;--subtle:#7e8392;--accent:#335bff;--accent-hover:#486dff;--shadow:0 16px 70px #0008;--input:#17181e}
[data-theme=light]{--bg:#f4f5f7;--nav:#fff;--panel:#fff;--card:#edeef2;--hover:#e1e4ed;--border:#dcdfe6;--text:#1e2028;--muted:#5e6471;--subtle:#787e8c;--shadow:0 16px 70px #14204426;--input:#fafbfc}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.4;transition:background .25s,color .25s}button,input,a{font:inherit}button,a{-webkit-tap-highlight-color:transparent}button{border:0;cursor:pointer;color:inherit;background:none}button:disabled{cursor:not-allowed;opacity:.45}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}input{color:var(--text);outline:none}button:focus-visible,a:focus-visible{outline:2px solid #7391ff;outline-offset:3px}button:focus:not(:focus-visible){outline:none}svg{flex-shrink:0}.i{width:18px;height:18px;vertical-align:middle;fill:none;stroke:currentColor;stroke-width:1.55;stroke-linecap:round;stroke-linejoin:round}.sprite{position:absolute;width:0;height:0;overflow:hidden}.muted{color:var(--muted)}.small{font-size:11px}.hidden,[hidden]{display:none!important}.row{display:flex;align-items:center;gap:7px}.grow{flex:1;min-width:0}.icon-btn{width:28px;height:28px;display:inline-flex;align-items:center;justify-content:center;border-radius:6px}.icon-btn:hover{background:var(--hover)}.primary{background:var(--accent);color:#fff;font-weight:700;border-radius:7px;min-height:32px;transition:background .18s,transform .18s}.primary:hover:not(:disabled){background:var(--accent-hover)}.primary:active:not(:disabled){transform:scale(.985)}.secondary{background:var(--card);border-radius:7px;min-height:32px;font-weight:700}.secondary:hover{background:var(--hover)}.full{width:100%}.text-button{color:var(--muted);font-size:11px;text-decoration:underline;padding:7px 3px}.badge{font-size:9px;letter-spacing:1.1px;border:1px solid #496bff60;color:#9eb2ff;background:#335bff16;border-radius:4px;padding:3px 5px;white-space:nowrap}.badge.live{border-color:#80909e40;color:var(--muted);background:var(--card)}
.topbar{height:36px;background:var(--nav);border-bottom:1px solid #ffffff08;display:flex;align-items:center;padding:0 15px;gap:24px;position:fixed;top:0;left:0;right:0;z-index:10}.brand{display:flex;align-items:center;gap:9px;white-space:nowrap}.wordmark{font-size:20px;font-weight:1000;letter-spacing:-1.4px;font-family:Arial Black,Arial,sans-serif;line-height:1}.wordmark b{display:inline-block;transform:rotate(-9deg)}.toplinks{display:flex;align-items:center;justify-content:space-between;gap:34px;min-width:300px}.toplinks a{font-size:11px;color:var(--muted)}.top-search{max-width:320px;flex:1;height:25px;border:1px solid var(--border);border-radius:6px;display:flex;align-items:center;gap:5px;padding:0 7px;color:var(--subtle)}.top-search input{background:none;border:0;width:100%;font-size:11px}.account{margin-left:auto;display:flex;align-items:center;gap:10px}.account-name{font-size:10px;color:var(--muted);max-width:135px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.side-user [data-profile-name]{min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.account .i{width:17px;height:17px}.mini-avatar{width:20px;height:20px;border-radius:50%;background:var(--card);display:grid;place-items:center}.top-balance{font-size:11px;font-weight:700}.sidebar{position:fixed;top:36px;bottom:0;width:190px;padding:12px 12px;background:var(--bg);z-index:5}.side-user{font-weight:bold;display:flex;gap:9px;align-items:center;margin:0 5px 12px}.side-user .mini-avatar{width:22px;height:22px}.side-links{display:grid;gap:2px}.side-links a,.side-links button{display:flex;align-items:center;gap:12px;height:32px;padding:6px 7px;font-size:12px;text-align:left;border-radius:6px;color:var(--muted);font-weight:600}.side-links a:hover,.side-links button:hover{background:var(--card);text-decoration:none;color:var(--text)}.side-links .i{width:18px;height:18px;color:var(--muted)}.subscribe{border:1px solid var(--border);border-radius:7px;margin-top:15px;padding:12px 8px;color:var(--muted);font-size:11px}.subscribe p{margin:9px 0}.subscribe a{text-decoration:underline}.side-foot{margin:20px 8px;color:var(--subtle);font-size:10px;line-height:1.6}.side-foot button{padding:0;color:inherit;text-decoration:underline}
.main{margin-left:190px;padding:80px 24px 70px;min-height:100dvh}.balance-bar{position:absolute;right:max(35px,calc((100vw - 1160px)/2));top:49px;display:flex;align-items:center;gap:10px;font-size:16px;font-weight:700}.balance-bar .send-top{font-size:10px;padding:5px 9px;border-radius:5px;color:var(--muted);background:var(--panel)}.balance-bar .send-top:hover{background:var(--card)}.balance-bar .send-top .i{width:13px;height:13px}.content{max-width:500px;margin:0 auto}.hero{text-align:center;margin:37px 0 32px}.hero h1{font-size:38px;line-height:1.05;letter-spacing:-1.3px;margin:0;font-weight:800}.hero p{font-size:10px;color:var(--subtle);margin:10px 0 0}.section-label{font-weight:700;font-size:13px;margin:0 0 8px}.packages{border:1px solid #ffffff08;border-radius:7px;padding:9px 12px;background:linear-gradient(120deg,#ffffff02,transparent)}.package{height:40px;display:flex;align-items:center;gap:6px}.package .value{font-size:18px;font-weight:750;white-space:nowrap;letter-spacing:-.6px}.package .i{width:18px;height:18px}.package .old{color:var(--subtle);font-size:13px;text-decoration:line-through;white-space:nowrap}.bonus{font-size:9px;padding:3px 6px;background:var(--panel);border-radius:10px;color:var(--muted);margin-left:10px;white-space:nowrap}.price{height:28px;width:134px;margin-left:auto;background:var(--card);border-radius:5px;display:grid;place-items:center;font-weight:700;font-size:11px}.price:hover{text-decoration:none;background:var(--hover)}.package:last-child .price{background:var(--accent);color:white}.package-note{margin:7px 0 0;font-size:9px;color:var(--subtle);text-align:right}.new-title{display:flex;align-items:center;gap:7px;font-size:19px;margin:25px 0 7px;font-weight:700}.new-title a{font-size:10px;color:var(--muted);margin-left:auto;text-decoration:underline}.plus-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.plus-card{border:1px solid var(--border);padding:12px 10px;border-radius:6px;min-height:124px;font-size:10px;color:var(--muted)}.plus-card strong{font-size:11px;color:var(--text)}.plus-card ul{padding:0;list-style:none;line-height:1.5;margin-top:16px}.plus-card li{display:flex;gap:5px;margin-bottom:9px}.plus-card .i{width:13px;height:13px}.bottom-access{margin:30px 0 0;display:flex;align-items:center;gap:8px;font-size:10px;color:var(--subtle)}.bottom-access .i{width:14px;height:14px}.bottom-access button{margin-left:auto;padding:0;color:var(--muted);text-decoration:underline}
.overlay{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;padding:20px;background:#0008;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);animation:fade .18s ease}.overlay.searching{backdrop-filter:blur(1px);-webkit-backdrop-filter:blur(1px)}.overlay .dialog{background:var(--panel);border:1px solid var(--border);box-shadow:var(--shadow);border-radius:11px;width:310px;max-height:calc(100dvh - 40px);overflow:hidden;animation:appear .22s cubic-bezier(.2,.8,.2,1);position:relative}.dialog-header{display:flex;align-items:center;gap:5px;height:44px;padding:9px 12px}.dialog-header h2{font-size:13px;letter-spacing:-.2px;margin:0;font-weight:750;display:flex;align-items:center;gap:4px}.dialog-header h2 .i{width:15px;height:15px}.dialog-balance{display:flex;align-items:center;gap:3px;margin-left:auto;font-size:10px;font-weight:700}.dialog-balance .i{width:12px;height:12px}.dialog-header .icon-btn{width:18px;height:20px;margin-left:3px;color:var(--muted)}.dialog-header .icon-btn .i{width:14px;height:14px}.dialog-body{max-height:calc(100dvh - 150px);overflow:auto;scrollbar-width:thin;scrollbar-color:#555963 transparent}.demo-strip{font-size:9px;color:var(--subtle);letter-spacing:.35px;text-align:center;margin:-2px 0 10px}.search-wrap{margin:0 13px 14px;position:relative}.search-wrap .i{position:absolute;left:10px;top:10px;width:14px;height:14px;color:var(--subtle)}.search-input{height:34px;width:100%;border:1px solid var(--border);border-radius:5px;padding:0 10px 0 30px;background:var(--input);font-size:11px}.search-input:focus{border-color:#5177ff;box-shadow:0 0 0 1px #5177ff}.results{min-height:211px;padding:0 13px 13px}.results-label{font-size:11px;font-weight:bold;color:var(--muted);margin:0 0 8px}.empty{font-size:11px;color:var(--muted);text-align:center;padding:18px 5px;line-height:1.6}.empty .i{width:26px;height:26px;color:var(--subtle);display:block;margin:10px auto}.result{display:flex;align-items:center;text-align:left;gap:9px;width:100%;padding:7px;border-radius:6px;min-height:48px}.result:hover{background:var(--card)}.avatar{object-fit:contain;background:transparent}.result .avatar{width:34px;height:34px;border-radius:50%;background:var(--card)}.result strong{font-size:11px;display:block;max-width:185px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.result span{font-size:10px;color:var(--muted)}.result .i{width:13px;height:13px;margin-left:auto;color:var(--subtle)}.skeleton{height:42px;background:linear-gradient(90deg,var(--card),var(--hover),var(--card));background-size:200% 100%;border-radius:6px;margin:7px 0;animation:shimmer 1.2s linear infinite}.chosen{padding:9px 13px 14px;text-align:center}.chosen .avatar{width:48px;height:48px;display:block;margin:0 auto 7px;animation:appear .25s ease}.chosen-name{font-weight:700;font-size:11px;margin:0 0 9px;overflow:hidden;text-overflow:ellipsis}.amount-box{display:flex;align-items:center;justify-content:center;margin:10px auto 14px;height:32px;gap:3px}.amount-box>.i{width:20px;height:20px}.amount-input{font-size:24px;font-weight:bold;letter-spacing:-.5px;width:145px;max-width:200px;text-align:center;border:0;padding:0 3px;background:none;appearance:textfield}.amount-input::placeholder{color:var(--text)}.amount-input::-webkit-inner-spin-button{display:none}.chips{display:flex;gap:5px;justify-content:center}.chip{display:flex;align-items:center;justify-content:center;gap:5px;min-width:48px;height:29px;border:1px solid transparent;background:var(--card);border-radius:7px;font-size:11px;font-weight:700}.chip .i{width:12px;height:12px}.chip:hover{background:var(--hover)}.chip.selected{border-color:var(--text);background:var(--hover)}.dialog-footer{border-top:1px solid #ffffff06;padding:13px 13px 11px;text-align:center}.dialog-footer .primary{font-size:11px;height:31px}.disclosure{font-size:9px;line-height:1.4;color:var(--muted);margin:10px 0 0}.form-error{font-size:11px;line-height:1.4;color:#ff9b9b;margin:8px 0 0;min-height:0}.form-error:empty{display:none}.back-line{display:flex;justify-content:center;margin-top:8px}.back-line button{font-size:10px;color:var(--subtle);padding:0}.back-line button:hover{color:var(--text)}.confirm-body{padding:0 13px 12px}.user-card{padding:10px 8px 10px;border-radius:10px;background:var(--card);text-align:center}.user-card .avatar{width:44px;height:44px;margin-bottom:3px}.user-card strong{display:block;font-size:11px;overflow-wrap:anywhere}.user-card .handle{font-size:11px;color:var(--muted);margin-top:2px}.user-meta{display:grid;gap:4px;margin-top:10px;font-size:9px;color:var(--muted)}.user-meta .i{width:11px;height:11px}.user-meta .row{justify-content:center;gap:4px}.summary-amount{display:flex;align-items:center;justify-content:center;gap:5px;border-radius:9px;background:var(--card);font-size:23px;font-weight:700;letter-spacing:-.4px;padding:8px;margin-top:8px}.summary-amount .i{width:19px;height:19px}.confirm-actions{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:8px;font-size:11px}.confirm-actions button{height:31px}.confirm-body .disclosure{text-align:center;margin-top:9px}.button-spinner{display:inline-block;width:13px;height:13px;border:2px solid #ffffff55;border-top-color:white;border-radius:50%;animation:spin .6s linear infinite;vertical-align:middle;margin-right:4px}.history-list{padding:0 13px 13px;min-height:160px}.history-item{display:flex;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid var(--border)}.history-item img{width:32px;height:32px}.history-item strong{font-size:11px}.history-item small{display:block;color:var(--subtle);font-size:9px;margin-top:3px}.history-amount{font-size:12px;font-weight:bold;white-space:nowrap}
.toast{position:fixed;top:50px;left:50%;transform:translate(-50%,-15px);opacity:0;z-index:90;pointer-events:none;display:flex;align-items:center;gap:7px;background:var(--panel);border:1px solid var(--border);box-shadow:0 4px 20px #0003;border-radius:7px;padding:10px 14px;font-size:11px;max-width:calc(100vw - 25px);transition:opacity .2s,transform .2s}.toast.on{opacity:1;transform:translate(-50%,0)}.toast .i{width:16px;height:16px;color:#73d7ac}.confetti{position:fixed;pointer-events:none;z-index:99;width:6px;height:10px;border-radius:2px;top:46%;left:50%;animation:confetti .85s ease-out forwards}.footer-watermark{position:fixed;bottom:10px;right:15px;font-size:9px;color:var(--subtle);z-index:12;letter-spacing:1px;pointer-events:none}.info-body{padding:0 17px 20px;font-size:12px;line-height:1.7;color:var(--muted)}.info-body a{color:#8ba5ff;text-decoration:underline}
@keyframes fade{from{opacity:0}to{opacity:1}}@keyframes appear{from{opacity:0;transform:translateY(8px) scale(.97)}to{opacity:1;transform:none}}@keyframes shimmer{to{background-position:-200% 0}}@keyframes spin{to{transform:rotate(360deg)}}@keyframes float{50%{transform:translateY(-5px) rotate(4deg)}}@keyframes confetti{to{transform:translate(var(--dx),var(--dy)) rotate(var(--rot));opacity:0}}
@media(min-width:1500px){.hero{margin-top:60px}.main{padding-top:100px}.content{max-width:550px}.package{height:44px}}
@media(max-width:1050px){.toplinks{min-width:auto;gap:22px}.topbar{gap:18px}.brand .badge{display:none}.account-name{display:none}.top-search{max-width:230px}.sidebar{width:166px}.main{margin-left:166px}.hero h1{font-size:35px}.balance-bar{right:24px}}
@media(max-width:700px){.topbar{height:45px;padding:0 12px;gap:12px}.toplinks,.sidebar,.top-search,.account-name,.account .mini-avatar,.top-balance{display:none}.brand .badge{display:block}.account{gap:7px}.wordmark{font-size:19px}.main{margin-left:0;padding:89px 18px 50px}.hero{margin:27px 0 35px}.hero h1{font-size:34px}.hero p{font-size:9px}.balance-bar{top:59px;right:20px;font-size:14px}.balance-bar .send-top{font-size:11px}.content{max-width:480px}.package{height:42px}.package .value{font-size:16px}.package .old{font-size:11px}.package .i{width:16px;height:16px}.bonus{font-size:8px;margin-left:4px;padding:2px 4px}.price{width:91px;font-size:11px}.new-title{font-size:17px}.plus-cards{gap:6px}.plus-card{padding:10px 7px;font-size:9px}.plus-card strong{font-size:10px}.overlay{padding:15px}.overlay .dialog{max-height:calc(100dvh - 30px)}.dialog-body{max-height:calc(100dvh - 120px)}.footer-watermark{font-size:8px;right:10px;bottom:max(7px,env(safe-area-inset-bottom))}.toast{top:54px}.topbar .icon-btn{width:27px;height:27px}.search-input{font-size:16px}.access-input{font-size:16px}.amount-input{font-size:24px}.plus-card li{margin-bottom:6px}.package-note{font-size:8px}}
/* GIFTER access screen — native CSS, inline SVG, no external visual assets. */
.access-scene{--login-bg:#090c13;--login-panel:#121722;--login-line:#273046;--login-text:#f2f5fc;--login-muted:#909bb1;--login-soft:#8795ad;--login-accent:#6685ff;--login-field:#0c111b;position:fixed;inset:0;z-index:60;overflow:auto;overscroll-behavior:contain;color:var(--login-text);background:var(--login-bg);isolation:isolate;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;transition:opacity .24s ease,visibility .24s ease}
.access-scene:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:-1;background:radial-gradient(ellipse at 17% 42%,#263c8529 0,transparent 47%),radial-gradient(ellipse at 88% 18%,#4f3e9220 0,transparent 40%),linear-gradient(135deg,#0d121e00,#0d121e50)}
.access-scene:after{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.18;background-image:linear-gradient(#6f8af509 1px,transparent 1px),linear-gradient(90deg,#6f8af509 1px,transparent 1px);background-size:64px 64px;mask-image:linear-gradient(180deg,#000,transparent 85%)}
.access-scene.is-leaving{opacity:0;visibility:hidden;pointer-events:none}.access-scene.is-leaving .login-card{transform:translateY(-6px);opacity:0}
.login-shell{width:min(1120px,100%);min-height:100dvh;padding:25px 36px 19px;margin:0 auto;display:grid;grid-template-rows:auto 1fr auto;gap:23px}
.login-nav{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:38px}
.login-brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px;letter-spacing:2.2px;line-height:1}
.login-brand-mark{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:linear-gradient(145deg,#7d96ff,#4164f1);color:#fff;box-shadow:inset 0 1px #ffffff40,0 4px 18px #335bff20}
.login-brand-mark .i{width:21px;height:21px;stroke-width:1.7}
.login-nav-right{display:flex;align-items:center;gap:20px}.login-help{font-size:12px;color:var(--login-muted);transition:color .15s}.login-help:hover{color:var(--login-text);text-decoration:none}
.login-theme{width:34px;height:34px;border:1px solid var(--login-line);border-radius:50%;display:grid;place-items:center;color:var(--login-muted);transition:background .18s,color .18s}.login-theme .i{width:15px;height:15px}.login-theme:hover{background:#6a82b018;color:var(--login-text)}
.login-stage{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:80px;align-items:center;padding:10px 0}
.login-story{padding:0 0 0 7px;animation:login-enter .6s ease both}
.login-eyebrow{display:flex;align-items:center;gap:8px;font-size:10px;letter-spacing:2.4px;font-weight:600;color:#8b9ac0;text-transform:uppercase;margin:0 0 21px}
.login-eyebrow:before{content:"";width:19px;height:1px;background:#708fff}
.login-story h1{font-size:clamp(42px,4.7vw,62px);line-height:1.08;letter-spacing:-2.8px;font-weight:750;margin:0;max-width:470px}
.login-story h1 span{display:block;color:#8ea8ff;background:linear-gradient(110deg,#95afff,#647cff 85%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.login-intro{font-size:14px;line-height:1.75;color:var(--login-muted);max-width:350px;margin:21px 0 0}
.login-art{height:235px;position:relative;margin:22px 0 8px;display:flex;align-items:center;justify-content:flex-start;perspective:900px;pointer-events:none}
.login-art:before{content:"";position:absolute;width:350px;height:120px;left:0;top:96px;border-radius:50%;background:#4c70ff1e;filter:blur(38px)}
.access-pass-back{position:absolute;left:30px;top:33px;width:300px;height:180px;border:1px solid #35436a;border-radius:17px;background:linear-gradient(135deg,#19253b,#111826);transform:rotate(7deg);opacity:.58}
.access-pass{position:relative;width:320px;height:190px;left:4px;border:1px solid #708ede68;border-radius:18px;background:linear-gradient(125deg,#293d71 0,#1c2c52 48%,#141d33 100%);box-shadow:0 20px 40px #0005,inset 0 1px #c3d4ff1c;transform:rotate(-7deg);overflow:hidden;animation:pass-float 7s ease-in-out infinite}
.access-pass:before{content:"";position:absolute;width:260px;height:260px;border:1px solid #b9d0ff14;border-radius:50%;right:-130px;top:-85px;box-shadow:0 0 0 26px #b9d0ff05,0 0 0 52px #b9d0ff04,0 0 0 78px #b9d0ff03}
.pass-top{display:flex;align-items:center;justify-content:space-between;position:relative;padding:21px 23px;font-size:10px;letter-spacing:2px;font-weight:bold;color:#d4dfff}.pass-top .i{width:17px;height:17px;opacity:.7}
.pass-art{position:absolute;right:34px;top:61px;transform:rotate(12deg);color:#a6beff}.pass-art .i{width:65px;height:65px;stroke-width:1.05;filter:drop-shadow(0 4px 16px #6485ff4d)}
.pass-code{position:absolute;left:23px;bottom:52px;color:#c2d0f0;font-size:14px;letter-spacing:2.8px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
.pass-bottom{position:absolute;left:23px;right:23px;bottom:20px;display:flex;justify-content:space-between;font-size:8px;letter-spacing:1.5px;color:#879abe}.pass-bottom b{color:#c8d8ff;font-weight:500}
.pass-token{position:absolute;left:240px;bottom:9px;padding:10px 13px;display:flex;align-items:center;gap:7px;border:1px solid #405581;background:#1d2a45;border-radius:10px;box-shadow:0 8px 24px #0004;color:#b8caff;font-size:10px;letter-spacing:.3px;transform:rotate(3deg);animation:token-float 7s ease-in-out infinite}.pass-token .i{width:15px;height:15px}
.login-features{display:flex;align-items:center;gap:20px;flex-wrap:wrap;color:var(--login-muted);font-size:11px;margin-top:8px}.login-features span{display:flex;align-items:center;gap:6px}.login-features .i{width:14px;height:14px;color:#8299d3}
.login-panel{min-width:0;animation:login-enter .65s .08s ease both}
.login-card{position:relative;padding:27px;border:1px solid var(--login-line);border-radius:22px;background:linear-gradient(145deg,#19223275,transparent 58%),var(--login-panel);box-shadow:0 20px 70px #0003,inset 0 1px #ffffff04;transition:transform .24s ease,opacity .24s ease,border-color .2s}
.login-card:before{content:"";position:absolute;left:36px;right:36px;top:-1px;height:1px;background:linear-gradient(90deg,transparent,#91aaff75,transparent)}
.login-card-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:23px}.login-key-mark{width:36px;height:36px;display:grid;place-items:center;border-radius:11px;border:1px solid #5372c84a;background:#4269e71c;color:#8faaff}.login-key-mark .i{width:18px;height:18px}.login-card-kicker{font-size:9px;color:var(--login-soft);letter-spacing:1.6px;font-weight:600}
.login-card h2{font-size:25px;line-height:1.2;letter-spacing:-.75px;margin:0;font-weight:700}.login-card-copy{color:var(--login-muted);font-size:12px;line-height:1.7;margin:9px 0 23px}
.key-label-row{display:flex;align-items:center;justify-content:space-between;margin:0 0 9px}.key-label-row label{font-size:11px;font-weight:600;letter-spacing:.2px;color:#b9c4d9}.key-paste{font-size:10px;color:#8da7ff;display:flex;align-items:center;gap:4px;padding:3px 0 3px 8px;border-radius:4px}.key-paste:hover{color:#c4d1ff}.key-paste .i{width:12px;height:12px}
.key-field{display:flex;align-items:center;gap:10px;padding:0 7px 0 14px;min-height:53px;position:relative;background:var(--login-field);border:1px solid var(--login-line);border-radius:11px;transition:border-color .2s,box-shadow .2s,background .2s}.key-field>.i{width:17px;height:17px;color:var(--login-soft);transition:color .2s}.key-field:focus-within{border-color:#7592ff;box-shadow:0 0 0 3px #5d7dff12;background:#101827}.key-field:focus-within>.i{color:#9cb2ff}
.access-input{border:0;background:transparent;min-width:0;width:100%;height:51px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:13px;letter-spacing:.4px;color:var(--login-text);padding:0;outline:none}.access-input::placeholder{color:#7e8aa1;font-size:12px;letter-spacing:.2px}.access-input:read-only{opacity:.6}
.key-visibility{width:34px;height:34px;flex:0 0 34px;color:var(--login-soft);display:grid;place-items:center;border-radius:7px;transition:background .2s,color .2s}.key-visibility:hover{color:var(--login-text);background:#8496b512}.key-visibility .i{width:17px;height:17px}
.key-hint{display:flex;align-items:center;gap:5px;font-size:10px;line-height:1.5;color:var(--login-soft);margin:9px 0 19px}.key-hint .i{width:11px;height:11px;flex-shrink:0}
.login-error{display:flex;align-items:flex-start;gap:8px;color:#f6a6ad;font-size:11px;line-height:1.6;padding:10px 12px;border:1px solid #b4475a45;background:#8b253618;border-radius:8px;margin:0 0 13px;animation:login-enter .2s ease}.login-error:before{content:"!";display:grid;place-items:center;flex:0 0 13px;width:13px;height:13px;border:1px solid currentColor;border-radius:50%;font-size:9px;line-height:1;margin-top:2px}.login-error:empty{display:none}
.login-card[data-state=error] .key-field{border-color:#b76377}.login-card[data-state=success] .key-field{border-color:#65ba9a;box-shadow:0 0 0 3px #65ba9a0c}
.login-submit{width:100%;height:49px;display:flex;align-items:center;justify-content:center;gap:10px;padding:0 18px;color:#fff;font-size:12px;font-weight:700;border:1px solid #9db0ff35;border-radius:10px;background:linear-gradient(115deg,#6886ff,#4466ee 72%);box-shadow:inset 0 1px #ffffff24,0 5px 20px #3158db25;transition:transform .18s,box-shadow .18s,filter .18s;position:relative;overflow:hidden}.login-submit:before{content:"";position:absolute;inset:0;transform:translateX(-115%);background:linear-gradient(100deg,transparent,#ffffff13,transparent);transition:transform .7s}.login-submit:hover:not(:disabled){box-shadow:inset 0 1px #ffffff30,0 8px 25px #3158db40;filter:brightness(1.07);transform:translateY(-1px)}.login-submit:hover:not(:disabled):before{transform:translateX(115%)}.login-submit:active:not(:disabled){transform:translateY(0)}.login-submit:disabled{opacity:1;cursor:wait}.login-submit .i{width:16px;height:16px}.login-submit .submit-arrow{position:absolute;right:17px;transition:transform .2s;opacity:.8}.login-submit:hover:not(:disabled) .submit-arrow{transform:translateX(3px)}.login-submit .button-spinner{width:14px;height:14px;margin:0}.login-card[data-state=success] .login-submit{background:linear-gradient(115deg,#3a8b75,#2c6f5d);border-color:#8cd6b52e;box-shadow:0 5px 20px #2d795020}
.login-separator{display:flex;align-items:center;gap:10px;margin:18px 0;font-size:10px;line-height:1;color:var(--login-soft)}.login-separator:before,.login-separator:after{content:"";height:1px;flex:1;background:var(--login-line)}
.login-buy{width:100%;min-height:43px;padding:9px 12px;display:flex;align-items:center;justify-content:center;gap:8px;background:#ffffff02;border:1px solid var(--login-line);border-radius:10px;font-size:12px;font-weight:600;transition:background .18s,border-color .18s}.login-buy:hover{background:#738dca0b;border-color:#465477;text-decoration:none}.login-buy .i{width:15px;height:15px;color:#f3cf8d}.buy-arrow{margin-left:auto!important;color:var(--login-muted)!important;width:13px!important;height:13px!important}.login-buy-label{flex:1}
.login-license-note{font-size:10px;line-height:1.6;color:var(--login-soft);text-align:center;margin:13px 0 0}.login-license-note b{font-weight:500;color:var(--login-muted)}
.login-pricing{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-top:12px}.login-price{padding:10px 9px;border:1px solid #6b7a9b16;border-radius:9px;display:flex;align-items:center;justify-content:space-between;gap:4px;background:#1c26300a;font-size:9px;color:var(--login-muted);white-space:nowrap}.login-price strong{color:#c0cce3;display:inline-flex;align-items:center;gap:3px;font-size:10px;font-weight:600}.login-price .i{width:11px;height:11px;color:#cbb785}
.preview-note{border:1px solid #6685ff45;border-radius:8px;padding:8px 10px;margin-bottom:17px;font-size:10px;color:#a4b6e1;background:#6685ff0d;line-height:1.7}.preview-note code{color:#d9e2ff;font-weight:600}
.login-bottom{display:flex;justify-content:space-between;align-items:center;gap:15px;font-size:9px;line-height:1.6;color:var(--login-soft)}.login-bottom span:first-child{display:flex;align-items:center;gap:5px}.login-bottom .i{width:12px;height:12px}.login-bottom b{font-weight:500;color:var(--login-muted)}
.access-scene button:focus-visible,.access-scene a:focus-visible{outline:2px solid #91aaff;outline-offset:4px}
[data-theme=light] .access-scene{--login-bg:#f1f4fa;--login-panel:#ffffff;--login-line:#d8e0ee;--login-text:#1e2a40;--login-muted:#61718a;--login-soft:#65748d;--login-accent:#4868dd;--login-field:#f7f9fd}
[data-theme=light] .access-scene:before{background:radial-gradient(ellipse at 17% 42%,#7999ef12 0,transparent 48%),radial-gradient(ellipse at 88% 18%,#b3a0dc14 0,transparent 40%)}
[data-theme=light] .login-card{background:linear-gradient(145deg,#fff,#fbfcff);box-shadow:0 20px 65px #4266ad12,inset 0 1px #fff}
[data-theme=light] .login-eyebrow{color:#6379a6}[data-theme=light] .login-story h1 span{background:linear-gradient(110deg,#5576da,#465ec9);-webkit-background-clip:text;background-clip:text}[data-theme=light] .key-label-row label{color:#4b5c77}[data-theme=light] .key-field:focus-within{background:#fff}[data-theme=light] .key-paste{color:#526ed0}[data-theme=light] .access-input::placeholder{color:#94a0b7}[data-theme=light] .login-price strong{color:#46597c}[data-theme=light] .login-price{border-color:#cbd5e34d;background:#ffffff40}[data-theme=light] .login-buy{background:#f7f9fd}[data-theme=light] .login-error{color:#aa4054;background:#c8485b0a}[data-theme=light] .preview-note{color:#576f9f}[data-theme=light] .preview-note code{color:#3d58a1}
@keyframes login-enter{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@keyframes pass-float{0%,100%{transform:translateY(0) rotate(-7deg)}50%{transform:translateY(-7px) rotate(-5.5deg)}}
@keyframes token-float{0%,100%{transform:translateY(0) rotate(3deg)}50%{transform:translateY(5px) rotate(1deg)}}
@media(min-height:850px) and (min-width:901px){.login-shell{gap:36px;padding-top:34px;padding-bottom:28px}.login-stage{gap:92px}.login-art{margin-top:33px;margin-bottom:16px}}
@media(max-width:1000px){.login-stage{gap:40px;grid-template-columns:minmax(0,1fr) 380px}.login-shell{padding-left:28px;padding-right:28px}.login-story h1{font-size:48px;letter-spacing:-2px}.login-features{gap:11px}.access-pass{width:290px;height:175px}.access-pass-back{width:275px;height:165px}.pass-token{left:205px}.login-art{height:220px}}
@media(max-width:820px){.login-shell{max-width:540px;padding:20px 26px 18px;gap:25px}.login-stage{grid-template-columns:minmax(0,1fr);gap:0;padding:5px 0;justify-items:center}.login-story{display:none}.login-panel{width:min(400px,100%)}.login-brand{font-size:16px;letter-spacing:2px}.login-brand-mark{width:31px;height:31px;border-radius:9px}.login-nav-right{gap:17px}.login-bottom{justify-content:center;flex-wrap:wrap;gap:5px 15px;text-align:center}.login-bottom span:last-child{font-size:8px}.login-card h2{font-size:26px}.access-input{font-size:16px}.login-price{padding:10px;font-size:9px}.login-price strong{font-size:10px}}
@media(max-width:390px){.login-shell{padding:18px 16px 15px;gap:21px}.login-card{padding:24px 21px;border-radius:19px}.login-card-top{margin-bottom:20px}.login-card h2{font-size:24px}.login-price{padding:9px 7px;font-size:9px}.login-card-copy{font-size:12px}.login-bottom{font-size:8px}.login-help{font-size:11px}.login-pricing{gap:5px}.login-buy{font-size:11px}}
@media(max-height:650px) and (min-width:821px){.login-shell{padding-top:17px;padding-bottom:14px;gap:14px}.login-stage{padding-top:0}.login-art{height:205px;margin-top:15px}.login-card{padding:22px 26px}.login-card-top{margin-bottom:15px}.login-card-copy{margin-bottom:18px}.login-story h1{font-size:49px}.login-pricing{margin-top:9px}.login-price{padding:8px}.login-story .login-intro{margin-top:15px}}

@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>
<script nonce="__NONCE__" src="https://telegram.org/js/telegram-web-app.js"></script>
</head><body>
<svg class="sprite" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs>
<symbol id="i-robux" viewBox="0 0 24 24"><path d="m12 2 8.7 5v10L12 22l-8.7-5V7z"/><path d="m12 6 5.2 3v6L12 18l-5.2-3V9z"/></symbol>
<symbol id="i-gift" viewBox="0 0 24 24"><path d="M4 11v10h16V11M3 7h18v5H3zM12 7v14M12 7C4 7 4 1 8 2c3 .6 4 5 4 5s1-4.4 4-5c4-1 4 5-4 5Z"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path d="m12 2 9 5v10l-9 5-9-5V7zM9 18V8l4-2 4 2v5l-4 2-4-2"/></symbol>
<symbol id="i-home" viewBox="0 0 24 24"><path d="m2 10 10-8 10 8M5 8v13h5v-7h4v7h5V8"/></symbol>
<symbol id="i-user" viewBox="0 0 24 24"><circle cx="12" cy="6" r="3.2"/><path d="M6 13q6-3 12 0v9H6z"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="7"/><path d="m16 16 5 5"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><path d="M3 4h18v13h-6l-3 4-3-4H3zM5 7l7 5 7-5"/></symbol>
<symbol id="i-users" viewBox="0 0 24 24"><circle cx="8" cy="6" r="3"/><circle cx="18" cy="7" r="2.5"/><path d="M2 21v-6q6-5 12 0v6zm14-8q4-2 6 2v6h-5"/></symbol>
<symbol id="i-avatar" viewBox="0 0 24 24"><circle cx="12" cy="4" r="2.5"/><path d="m7 9-3 5 3 2 3-4v4l-2 6m6 0-1-6v-4l4 4 3-2-4-5z"/></symbol>
<symbol id="i-bag" viewBox="0 0 24 24"><path d="M4 8h16v13H4zM8 8V5q4-6 8 0v3M4 12h16M10 12v3h4v-3"/></symbol>
<symbol id="i-trade" viewBox="0 0 24 24"><path d="M3 7h17m-5-5 5 5-5 5M21 17H4m5-5-5 5 5 5"/></symbol>
<symbol id="i-blog" viewBox="0 0 24 24"><path d="m3 21 4-8L18 2l4 4-11 11zm4-8 4 4M3 21l7-2M14 6l4 4"/></symbol>
<symbol id="i-store" viewBox="0 0 24 24"><path d="M3 8h18l-3-5H6zM3 8v4q3 3 6 0 3 3 6 0 3 3 6 0V8M5 14v8h14v-8M9 22v-6h6v6"/></symbol>
<symbol id="i-card" viewBox="0 0 24 24"><path d="M2 7h20v14H2zM2 11h20M6 16h5M9 7C2 7 6 0 9 3l3 4c8 0 5-7 2-4l-2 4"/></symbol>
<symbol id="i-bell" viewBox="0 0 24 24"><path d="M4 17h16l-2-4V8a6 6 0 0 0-12 0v5zM9 21h6M12 2V1"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12 2 2M4 20l2-2M18 6l2-2"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24"><path d="M20 14A9 9 0 0 1 10 3a9 9 0 1 0 10 11Z"/></symbol>
<symbol id="i-up" viewBox="0 0 24 24"><path d="M12 17V3m-5 5 5-5 5 5M4 18v4h16v-4"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="m5 5 14 14M5 19 19 5"/></symbol>
<symbol id="i-chevron" viewBox="0 0 24 24"><path d="m9 5 7 7-7 7"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m7 12 3 3 7-7"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/></symbol>
<symbol id="i-key" viewBox="0 0 24 24"><circle cx="8" cy="8" r="5"/><path d="m12 12 9 9m-5-5 3-3m0 6 3-3"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="m12 2 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z" fill="currentColor" stroke="none"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="m12 2 9 3v6c0 5-4 8-9 11-5-3-9-6-9-11V5zM8 12l3 3 5-6"/></symbol>
<symbol id="i-tag" viewBox="0 0 24 24"><path d="m3 12 9-9h8v8l-9 10z"/><circle cx="16" cy="7" r="1"/></symbol>
<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-11v1"/></symbol>
<symbol id="i-logout" viewBox="0 0 24 24"><path d="M10 3H3v18h7m-1-9h13m-5-5 5 5-5 5"/></symbol>
<symbol id="i-eye" viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></symbol>
<symbol id="i-eye-off" viewBox="0 0 24 24"><path d="m3 3 18 18M10.6 5.1A12.3 12.3 0 0 1 12 5c6.4 0 10 7 10 7a18 18 0 0 1-3.1 3.9M6.5 6.5A19.5 19.5 0 0 0 2 12s3.6 7 10 7a11.8 11.8 0 0 0 5.5-1.5M9.9 9.9a3 3 0 0 0 4.2 4.2"/></symbol>
<symbol id="i-clipboard" viewBox="0 0 24 24"><path d="M9 5H6a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-3"/><rect x="8" y="2" width="8" height="6" rx="2"/></symbol>
<symbol id="i-arrow-right" viewBox="0 0 24 24"><path d="M4 12h16m-6-6 6 6-6 6"/></symbol>
<symbol id="i-arrow-up-right" viewBox="0 0 24 24"><path d="M6 18 18 6M6 6h12v12"/></symbol>
</defs></svg>
<div id="page">
<header class="topbar"><a class="brand" href="/" aria-label="Gifter demo home"><span class="wordmark">R<b>O</b>BLOX</span><span class="badge">GIFTER DEMO</span></a>
<nav class="toplinks" aria-label="Roblox links"><a href="https://www.roblox.com/charts" target="_blank" rel="noopener">Charts</a><a href="https://www.roblox.com/catalog" target="_blank" rel="noopener">Marketplace</a><a href="https://create.roblox.com/" target="_blank" rel="noopener">Create</a><a href="https://www.roblox.com/upgrades/robux" target="_blank" rel="noopener">Robux</a></nav>
<form class="top-search" id="top-search"><svg class="i"><use href="#i-search"/></svg><input id="top-query" placeholder="Search" aria-label="Search Roblox users" autocomplete="off" maxlength="32"></form>
<div class="account"><span class="mini-avatar"><svg class="i"><use href="#i-user"/></svg></span><span class="account-name" data-profile-name>Gifter Studio</span><button class="icon-btn" id="history-top" title="Demo history" aria-label="Demo history"><svg class="i"><use href="#i-bell"/></svg></button><span class="row top-balance"><svg class="i"><use href="#i-robux"/></svg><span data-balance>—</span></span><button class="icon-btn" id="theme" title="Switch theme" aria-label="Switch theme"><svg class="i"><use href="#i-sun"/></svg></button></div></header>
<aside class="sidebar"><div class="side-user"><span class="mini-avatar"><svg class="i"><use href="#i-user"/></svg></span><span data-profile-name>Gifter Studio</span></div><nav class="side-links" id="side-links" aria-label="Navigation"></nav><div class="subscribe"><svg class="i"><use href="#i-plus"/></svg><p>More fun for less Robux. Subscribe to Roblox Plus.</p><a href="https://www.roblox.com/plus" target="_blank" rel="noopener">Learn more on Roblox</a></div><div class="side-foot">Independent visual demo.<br>No real Robux transfers.<br><button id="about-side">About this interface</button></div></aside>
<main class="main"><div class="balance-bar"><span class="row"><svg class="i"><use href="#i-robux"/></svg><span data-balance>—</span></span><button class="send-top row" id="open-send"><svg class="i"><use href="#i-up"/></svg>Send</button></div><div class="content"><section class="hero"><h1>Enjoy up to 25%<br>more Robux</h1><p>Reference interface · visual demo</p></section><h2 class="section-label">Robux packages</h2><div class="packages" id="packages"></div><p class="package-note">Illustrative reference prices. Purchase buttons open the official Roblox website.</p>
<div class="new-title"><svg class="i"><use href="#i-plus"/></svg>New on Roblox<a href="https://www.roblox.com/plus" target="_blank" rel="noopener">Learn more</a></div><div class="plus-cards"><div class="plus-card"><strong>Roblox Plus</strong><ul><li><svg class="i"><use href="#i-tag"/></svg>Discover membership benefits</li><li><svg class="i"><use href="#i-gift"/></svg>Explore on Roblox</li></ul></div><div class="plus-card"><strong>Plus 500</strong><ul><li><svg class="i"><use href="#i-plus"/></svg>Reference plan layout</li><li><svg class="i"><use href="#i-robux"/></svg>See official availability</li></ul></div><div class="plus-card"><strong>Plus 1000</strong><ul><li><svg class="i"><use href="#i-plus"/></svg>Reference plan layout</li><li><svg class="i"><use href="#i-robux"/></svg>See official availability</li></ul></div></div>
<div class="bottom-access"><svg class="i"><use href="#i-key"/></svg><span id="access-status">Access by license key</span><button id="logout" hidden>Sign out</button></div></div></main>
</div>
<div class="footer-watermark">GIFTER · DEMO</div>
<div id="overlay" class="overlay hidden" role="presentation"><section class="dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title"><header class="dialog-header"><h2 id="dialog-title"><svg class="i"><use href="#i-plus"/></svg><span id="dialog-label">Send Robux</span></h2><span class="dialog-balance"><svg class="i"><use href="#i-robux"/></svg><span data-balance>—</span></span><button id="close-dialog" class="icon-btn" aria-label="Close"><svg class="i"><use href="#i-close"/></svg></button></header><div id="dialog-content" class="dialog-body"></div></section></div>
<section id="access-overlay" class="access-scene" lang="ru" aria-label="Вход в Gifter">
  <div class="login-shell" role="dialog" aria-modal="true" aria-labelledby="access-title">
    <header class="login-nav">
      <div class="login-brand"><span class="login-brand-mark"><svg class="i" aria-hidden="true"><use href="#i-gift"/></svg></span>GIFTER</div>
      <nav class="login-nav-right" aria-label="Помощь и оформление">
        <a id="login-support" class="login-help" href="#">Поддержка</a>
        <button id="login-theme" class="login-theme" type="button" aria-label="Переключить тему"><svg class="i" aria-hidden="true"><use href="#i-sun"/></svg></button>
      </nav>
    </header>
    <div class="login-stage">
      <div class="login-story">
        <p class="login-eyebrow">ТВОЁ ПРОСТРАНСТВО</p>
        <h1>Один ключ.<span>Весь Gifter.</span></h1>
        <p class="login-intro">Находи игроков, открывай профили<br>и исследуй интерфейс в своём темпе.</p>
        <div class="login-art" aria-hidden="true">
          <div class="access-pass-back"></div>
          <div class="access-pass">
            <div class="pass-top"><span>GIFTER ACCESS</span><svg class="i"><use href="#i-plus"/></svg></div>
            <div class="pass-art"><svg class="i"><use href="#i-key"/></svg></div>
            <div class="pass-code">GF · •••••• · ••••••</div>
            <div class="pass-bottom"><span>YOUR PERSONAL PASS</span><b>DEMO EDITION</b></div>
          </div>
          <div class="pass-token"><svg class="i"><use href="#i-shield"/></svg>Твой личный доступ</div>
        </div>
        <div class="login-features"><span><svg class="i" aria-hidden="true"><use href="#i-search"/></svg>Поиск игроков</span><span><svg class="i" aria-hidden="true"><use href="#i-user"/></svg>Профили</span><span><svg class="i" aria-hidden="true"><use href="#i-gift"/></svg>Gifter DEMO</span></div>
      </div>
      <div class="login-panel">
        <section class="login-card" id="login-card" data-state="idle" aria-busy="false">
          <div class="login-card-top"><span class="login-key-mark"><svg class="i" aria-hidden="true"><use href="#i-key"/></svg></span><span class="login-card-kicker">PERSONAL ACCESS</span></div>
          <h2 id="access-title">Открыть Gifter</h2>
          <p class="login-card-copy">Твой доступ начинается здесь.<br>Введи ключ, полученный в Telegram.</p>
          <div id="preview-note" class="preview-note" hidden>Локальный просмотр. Для входа: <code>DEMO-LOCAL</code></div>
          <form id="key-form" novalidate>
            <div class="key-label-row"><label for="key">Ключ доступа</label><button class="key-paste" id="paste-key" type="button"><svg class="i" aria-hidden="true"><use href="#i-clipboard"/></svg>Вставить</button></div>
            <div class="key-field">
              <svg class="i" aria-hidden="true"><use href="#i-key"/></svg>
              <input class="access-input" id="key" type="password" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="100" placeholder="GF-XXXXXX-XXXXXX-…" aria-describedby="key-hint auth-error" aria-invalid="false" required>
              <button class="key-visibility" id="show-key" type="button" aria-label="Показать ключ" aria-pressed="false"><svg class="i" aria-hidden="true"><use href="#i-eye"/></svg></button>
            </div>
            <p class="key-hint" id="key-hint"><svg class="i" aria-hidden="true"><use href="#i-clock"/></svg>Срок доступа начинается с первой активации</p>
            <div id="auth-error" class="login-error" role="alert" aria-live="polite"></div>
            <button class="login-submit" id="activate" type="submit"><span>Войти в Gifter</span><svg class="i submit-arrow" aria-hidden="true"><use href="#i-arrow-right"/></svg></button>
          </form>
          <div class="login-separator">Ещё нет ключа?</div>
          <a id="buy-link" class="login-buy" href="#"><svg class="i" aria-hidden="true"><use href="#i-star"/></svg><span class="login-buy-label">Выбрать доступ в Telegram</span><svg class="i buy-arrow" aria-hidden="true"><use href="#i-arrow-up-right"/></svg></a>
          <p class="login-license-note">Покупка через <b>Telegram Stars</b><br>Доступ к DEMO-интерфейсу, без перевода Robux</p>
        </section>
        <div id="price-summary" class="login-pricing" aria-label="Тарифы доступа">
          <div class="login-price"><span>1 час</span><strong>5 <svg class="i" aria-label="Stars"><use href="#i-star"/></svg></strong></div>
          <div class="login-price"><span>2 часа</span><strong>15 <svg class="i" aria-label="Stars"><use href="#i-star"/></svg></strong></div>
          <div class="login-price"><span>1 день</span><strong>30 <svg class="i" aria-label="Stars"><use href="#i-star"/></svg></strong></div>
          <div class="login-price"><span>2 дня</span><strong>50 <svg class="i" aria-label="Stars"><use href="#i-star"/></svg></strong></div>
          <div class="login-price"><span>5 дней</span><strong>100 <svg class="i" aria-label="Stars"><use href="#i-star"/></svg></strong></div>
          <div class="login-price"><span>Навсегда</span><strong>400 <svg class="i" aria-label="Stars"><use href="#i-star"/></svg></strong></div>
        </div>
      </div>
    </div>
    <footer class="login-bottom"><span><svg class="i" aria-hidden="true"><use href="#i-shield"/></svg>Пароль и cookie Roblox не требуются</span><span><b>GIFTER DEMO</b> · Независимый проект</span></footer>
  </div>
</section>
<div class="toast" id="toast" role="status" aria-live="polite"><svg class="i"><use href="#i-check"/></svg><span></span></div>
<script nonce="__NONCE__">
'use strict';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const icon=n=>`<svg class="i" aria-hidden="true"><use href="#i-${n}"/></svg>`;
const escapeText=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const number=n=>new Intl.NumberFormat('en-US').format(n),avatar=id=>`/api/avatar/${Number(id)}`;
const state={me:null,token:null,config:null,player:null,amount:0,step:null,requestId:null,busy:false,searchSeq:0,lastFocus:null,authRevision:0,expiryDeadline:Infinity,expiryWallDeadline:Infinity};
let debounce,toastTimer,searchAbort,expiryTimer;
const tg=window.Telegram?.WebApp;
try{tg?.ready();tg?.expand()}catch(e){}
try{document.documentElement.dataset.theme=localStorage.getItem('gifter_theme')||'dark'}catch(e){}
function setTheme(){const dark=document.documentElement.dataset.theme==='dark';for(const selector of ['#theme','#login-theme'])$(selector).innerHTML=icon(dark?'sun':'moon');try{tg?.setHeaderColor(dark?'#191a1f':'#ffffff');tg?.setBackgroundColor(dark?'#111215':'#f4f5f7')}catch(e){}}
function cycleTheme(){document.documentElement.dataset.theme=document.documentElement.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem('gifter_theme',document.documentElement.dataset.theme)}catch(e){}setTheme()}
setTheme();$('#theme').onclick=cycleTheme;$('#login-theme').onclick=cycleTheme;
const links=[['home','Home','https://www.roblox.com/home'],['user','Profile','https://www.roblox.com/home'],['plus','Roblox Plus','https://www.roblox.com/plus'],['mail','Messages','https://www.roblox.com/my/messages'],['users','Friends','https://www.roblox.com/users/friends'],['avatar','Avatar','https://www.roblox.com/my/avatar'],['bag','Inventory','https://www.roblox.com/home'],['trade','Trade','https://www.roblox.com/trades'],['users','Communities','https://www.roblox.com/communities'],['blog','Blog','https://corp.roblox.com/newsroom'],['store','Official Store','https://shop.roblox.com/'],['card','Buy Gift Cards','https://www.roblox.com/giftcards']];
$('#side-links').innerHTML=links.map(([ic,label,url])=>`<a href="${url}" target="_blank" rel="noopener">${icon(ic)}${label}</a>`).join('');
const packs=[[24000,20000,4000,'199.99'],[11000,10000,1000,'99.99'],[5250,4500,750,'49.99'],[3625,3000,625,'34.99'],[2000,1700,300,'19.99'],[1500,1200,300,'14.99'],[1000,800,200,'9.99'],[500,400,100,'4.99']];
$('#packages').innerHTML=packs.map(([n,old,bonus,price])=>`<div class="package"><span class="row value">${icon('robux')}${number(n).replaceAll(',',' ')}</span><span class="old">${number(old).replaceAll(',',' ')}</span><span class="bonus">+ ${number(bonus)} more</span><a class="price" href="https://www.roblox.com/upgrades/robux" target="_blank" rel="noopener" aria-label="Open official Roblox shop — illustrative ${price} dollars">${price} $</a></div>`).join('');
async function api(path,body,signal){const revision=state.authRevision;const opts={credentials:'same-origin',headers:state.token?{Authorization:'Bearer '+state.token}:{},signal};if(body!==undefined){opts.method='POST';opts.headers['Content-Type']='application/json';opts.body=JSON.stringify(body)}const r=await fetch(path,opts);let data;try{data=await r.json()}catch(e){throw Error('Сервер временно недоступен. Повторите попытку.')}if(!r.ok){if(r.status===401&&state.me&&revision===state.authRevision)lock();throw Error(data.error||'Ошибка запроса')}return data}
function toast(text){$('#toast span').textContent=text;$('#toast').classList.add('on');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('on'),4200)}
function updateBalance(n){if(state.me)state.me.balance=n;$$('[data-balance]').forEach(e=>e.textContent=number(n))}
function remainingAccessMs(){
  return Math.min(state.expiryDeadline-performance.now(),state.expiryWallDeadline-Date.now());
}
function expireAccess(){
  const licenseExpired=state.me?.expires_at!==null&&state.me?.expires_at<=state.me?.session_expires_at;
  lock();
  setLoginError(licenseExpired?'Срок ключа истёк. Доступ к панели закрыт. Получите новый ключ через /stars или у администратора.':'Сессия завершена. Введите свой действующий ключ снова.');
}
function scheduleExpiry(me,requestStarted){
  clearTimeout(expiryTimer);
  const end=Math.min(me.expires_at??Infinity,me.session_expires_at);
  const remaining=Math.max(0,(end-me.server_time)*1000-(performance.now()-requestStarted));
  state.expiryDeadline=performance.now()+remaining;
  state.expiryWallDeadline=Date.now()+remaining;
  const check=()=>{
    if(!state.me)return;
    const left=remainingAccessMs();
    if(left<=0){expireAccess();return}
    expiryTimer=setTimeout(check,Math.min(left,2147483647));
  };
  check();
}
function updateExpiry(){
  if(!state.me)return;
  const left=remainingAccessMs();
  if(left<=0){expireAccess();return}
  if(state.me.expires_at===null){$('#access-status').textContent='Lifetime access · demo balance';return}
  const seconds=Math.ceil(left/1000),hours=Math.floor(seconds/3600),minutes=Math.floor(seconds%3600/60);
  $('#access-status').textContent=`Access: ${hours}h ${minutes}m ${seconds%60}s remaining · demo balance`;
}
async function loadMe(reveal=true){
  const version=state.authRevision,started=performance.now();
  const me=await api('/api/me');
  if(version!==state.authRevision)return;
  state.me=me;updateBalance(me.balance);
  $$('[data-profile-name]').forEach(e=>{e.textContent=me.nickname||'Gifter Studio';e.title=e.textContent});
  $('#logout').hidden=false;scheduleExpiry(me,started);updateExpiry();
  if(state.me&&state.step==='amount')updateAmount();
  if(reveal&&state.me)revealApp();
}
function lock(){
  clearTimeout(loginRevealTimer);clearTimeout(expiryTimer);state.authRevision++;state.me=null;state.token=null;state.busy=false;closeDialog();
  $('#access-overlay').classList.remove('hidden','is-leaving');$('#page').inert=true;
  state.player=null;state.requestId=null;$('#dialog-content').innerHTML='';$$('[data-profile-name]').forEach(e=>e.textContent='Gifter Studio');
  $('#logout').hidden=true;$('#access-status').textContent='Access by license key';$$('[data-balance]').forEach(e=>e.textContent='—');
  setLoginError('');setLoginState('idle');$('#key').value='';$('#key').type='password';
  $('#show-key').setAttribute('aria-pressed','false');$('#show-key').setAttribute('aria-label','Показать ключ');$('#show-key').innerHTML=icon('eye');$('#key').focus();
}
$('#page').inert=true;
let loginRevealTimer;
function setLoginState(mode,label=''){
  const card=$('#login-card'),b=$('#activate'),busy=mode==='checking'||mode==='success';
  card.dataset.state=mode;card.setAttribute('aria-busy',String(mode==='checking'));
  b.disabled=busy;$('#key').readOnly=busy;$('#paste-key').disabled=busy;$('#show-key').disabled=busy;
  if(mode==='checking')b.innerHTML='<span class="button-spinner" aria-hidden="true"></span><span>'+escapeText(label||'Проверяем ключ…')+'</span>';
  else if(mode==='success')b.innerHTML=icon('check')+'<span>Доступ открыт</span>';
  else b.innerHTML='<span>Войти в Gifter</span><svg class="i submit-arrow" aria-hidden="true"><use href="#i-arrow-right"/></svg>';
}
function setLoginError(message){
  $('#auth-error').textContent=message||'';$('#key').setAttribute('aria-invalid',String(Boolean(message)));
  if(message)setLoginState('error');
}
function revealApp(){
  const root=$('#access-overlay');
  if(root.classList.contains('hidden')||root.classList.contains('is-leaving'))return;
  root.classList.add('is-leaving');$('#page').inert=!$('#overlay').classList.contains('hidden');
  loginRevealTimer=setTimeout(()=>{if(state.me){root.classList.add('hidden');root.classList.remove('is-leaving');if(state.step===null)$('#open-send').focus()}},240);
}
$('#key').addEventListener('input',()=>{if($('#login-card').dataset.state==='error'){setLoginError('');setLoginState('idle')}});
$('#show-key').onclick=()=>{
  const show=$('#key').type==='password';$('#key').type=show?'text':'password';
  $('#show-key').setAttribute('aria-pressed',String(show));$('#show-key').setAttribute('aria-label',show?'Скрыть ключ':'Показать ключ');
  $('#show-key').innerHTML=icon(show?'eye-off':'eye');
};
$('#paste-key').onclick=async()=>{
  try{
    if(!navigator.clipboard?.readText)throw Error('Clipboard unavailable');
    const text=await navigator.clipboard.readText();
    if($('#activate').disabled)return;
    if(!text.trim()){toast('Буфер обмена пуст');return}
    $('#key').value=text.replace(/\s+/g,'').slice(0,100);setLoginError('');setLoginState('idle');$('#key').focus();
  }catch(e){toast('Вставь ключ вручную: нажми на поле и выбери «Вставить»')}
};
$('#key-form').onsubmit=async e=>{
  e.preventDefault();if($('#activate').disabled)return;
  const key=$('#key').value.replace(/\s+/g,'').trim();
  setLoginError('');
  if(!key){setLoginError('Сначала введи ключ доступа. Он находится в сообщении бота после покупки.');$('#key').focus();return}
  setLoginState('checking');state.authRevision++;
  try{
    const session=await api('/api/activate',{key});state.token=session.session_token;
    await loadMe(false);if(!state.me)return;setLoginState('success');$('#key').value='';
    await new Promise(resolve=>setTimeout(resolve,420));
    if(state.me){revealApp();toast('Доступ активирован')}
  }catch(e){state.token=null;setLoginError(e.message)}
};
$('#login-support').onclick=e=>{
  e.preventDefault();const account=state.config?.support||state.config?.bot;
  if(!account){toast(state.config?.preview?'Локальный просмотр: поддержка не подключена':'Бот подключается. Попробуй открыть поддержку чуть позже.');return}
  const url=`https://t.me/${account}`;
  if(tg?.openTelegramLink)tg.openTelegramLink(url);else window.open(url,'_blank','noopener,noreferrer');
  if(!state.config.support)toast('Для поддержки отправь боту команду /paysupport');
};
$('#logout').onclick=async()=>{try{await api('/api/logout',{});lock()}catch(e){toast(e.message)}};
$('#buy-link').onclick=e=>{if(!state.config?.bot){e.preventDefault();toast(state.config?.preview?'В локальном просмотре покупка отключена. Введите DEMO-LOCAL.':'Бот подключается. Обновите страницу через несколько секунд.');return}if(tg?.openTelegramLink){e.preventDefault();tg.openTelegramLink(`https://t.me/${state.config.bot}?start=stars`)}};
function show(step,label='Send Robux'){state.step=step;const overlay=$('#overlay');overlay.classList.remove('hidden');overlay.classList.toggle('searching',step==='search');$('#dialog-label').textContent=label;$('#page').inert=true;$('#close-dialog').disabled=false;tg?.BackButton?.show();}
function closeDialog(){if(state.busy)return;clearTimeout(debounce);searchAbort?.abort();state.searchSeq++;$('#overlay').classList.add('hidden');state.step=null;$('#page').inert=!$('#access-overlay').classList.contains('hidden');tg?.BackButton?.hide();state.lastFocus?.focus?.()}
$('#close-dialog').onclick=closeDialog;$('#overlay').onclick=e=>{if(e.target===$('#overlay'))closeDialog()};tg?.BackButton?.onClick(()=>{if(state.step==='confirm')amountStep();else if(state.step==='amount')openSearch();else closeDialog()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeDialog();if(e.key==='Tab'){const root=!$('#access-overlay').classList.contains('hidden')?$('#access-overlay'):!$('#overlay').classList.contains('hidden')?$('#overlay'):null;if(!root)return;const els=[...root.querySelectorAll('button:not(:disabled),input:not(:disabled),a[href]')].filter(x=>x.offsetParent!==null);if(!els.length)return;const first=els[0],last=els.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}});
function requireAccess(){if(state.me)updateExpiry();if(!state.me){$('#key').focus();return false}return true}
async function openSearch(query=''){if(!requireAccess())return;state.lastFocus=document.activeElement;state.player=null;state.amount=0;state.requestId=null;show('search');$('#dialog-content').innerHTML=`<div class="demo-strip">DEMO · no real Robux transfers</div><div class="search-wrap">${icon('search')}<input class="search-input" id="user-query" placeholder="Search username or user ID" aria-label="Search username or user ID" autocomplete="off" maxlength="32"></div><div class="results"><div class="results-label" id="results-label">Recent recipients</div><div id="results"><div class="empty">Search for a Roblox player</div></div></div>`;const input=$('#user-query');input.value=query;input.oninput=()=>{clearTimeout(debounce);searchAbort?.abort();state.searchSeq++;const q=input.value.trim();if(!q){$('#results-label').textContent='Recent recipients';recent();return}if(q.replace(/^@/,'').length<3&&!/^\d+$/.test(q)){$('#results').innerHTML='<div class="empty">Type at least 3 characters</div>';return}debounce=setTimeout(()=>search(q),350)};setTimeout(()=>input.focus(),80);if(query)search(query);else recent()}
$('#open-send').onclick=()=>openSearch();$('#top-search').onsubmit=e=>{e.preventDefault();openSearch($('#top-query').value)};
async function recent(){const seq=++state.searchSeq;try{const d=await api('/api/history');if(seq!==state.searchSeq||state.step!=='search')return;const seen=new Set();const rows=d.gifts.filter(g=>{if(seen.has(g.recipient_id))return false;seen.add(g.recipient_id);return true}).slice(0,5).map(g=>({id:g.recipient_id,name:g.recipient_name,displayName:g.recipient_name}));renderResults(rows,'No recent recipients')}catch(e){if(seq===state.searchSeq&&state.step==='search')$('#results').innerHTML='<div class="empty">Search for a Roblox player</div>'}}
async function search(q){const seq=++state.searchSeq;searchAbort?.abort();searchAbort=new AbortController();$('#results-label').textContent='Search results';$('#results').innerHTML='<div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div>';try{const d=await api('/api/users?q='+encodeURIComponent(q),undefined,searchAbort.signal);if(seq===state.searchSeq&&state.step==='search')renderResults(d.users,'No players found')}catch(e){if(e.name!=='AbortError'&&seq===state.searchSeq&&state.step==='search')$('#results').innerHTML=`<div class="empty">${escapeText(e.message)}</div>`}}
function renderResults(rows,empty){const root=$('#results');if(!root)return;if(!rows.length){root.innerHTML=`<div class="empty">${escapeText(empty)}</div>`;return}root.innerHTML=rows.map((p,i)=>`<button class="result" data-index="${i}"><img class="avatar" src="${avatar(p.id)}" alt="" loading="lazy"><div class="grow"><strong>${escapeText(p.displayName)}${p.hasVerifiedBadge?' ✓':''}</strong><span>@${escapeText(p.name)}</span></div>${icon('chevron')}</button>`).join('');root.querySelectorAll('button').forEach(b=>b.onclick=()=>choose(rows[Number(b.dataset.index)]))}
async function choose(p){if(!requireAccess()||state.busy)return;state.player=p;state.amount=0;state.requestId=null;amountStep();const id=p.id;try{const full=await api(`/api/user/${id}`);if(state.player?.id===id){state.player=full;if(state.step==='confirm')confirmStep()}}catch(e){if(state.player?.id===id)state.player.created=''}}
function amountStep(){if(!requireAccess()||!state.player)return;show('amount');const p=state.player;$('#dialog-content').innerHTML=`<div class="demo-strip">DEMO · no real Robux transfers</div><div class="chosen"><img class="avatar" src="${avatar(p.id)}" alt="Avatar of ${escapeText(p.displayName)}"><div class="chosen-name">${escapeText(p.displayName)}</div><div class="amount-box">${icon('robux')}<input class="amount-input" id="amount" inputmode="numeric" autocomplete="off" aria-label="Demo amount" placeholder="0" maxlength="10" value="${state.amount||''}"></div><div class="chips">${[25,50,100,200].map(n=>`<button class="chip ${state.amount===n?'selected':''}" data-amount="${n}">${icon('robux')}${n}</button>`).join('')}</div><div class="form-error" id="amount-error" role="alert"></div><div class="back-line"><button id="change-player">Change player</button></div></div><footer class="dialog-footer"><button class="primary full" id="next">Next</button><p class="disclosure">Visual demonstration · no Robux will arrive</p></footer>`;const input=$('#amount');input.oninput=()=>{input.value=input.value.replace(/\D/g,'').slice(0,10);state.amount=Number(input.value);state.requestId=null;updateAmount()};input.onkeydown=e=>{if(e.key==='Enter'&&!$('#next').disabled)confirmStep()};$$('[data-amount]').forEach(b=>b.onclick=()=>{state.amount=Number(b.dataset.amount);state.requestId=null;input.value=state.amount;updateAmount()});$('#next').onclick=confirmStep;$('#change-player').onclick=()=>openSearch();updateAmount();setTimeout(()=>input.focus(),70)}
function updateAmount(){const n=state.amount;$$('.chip').forEach(b=>b.classList.toggle('selected',Number(b.dataset.amount)===n));$('#next').disabled=!Number.isInteger(n)||n<=0||n>state.me.balance;$('#amount-error').textContent=n>state.me.balance?'Недостаточно демонстрационного баланса.':'';$('#amount').style.width=Math.max(40,String(n||0).length*15+8)+'px'}
function confirmStep(){if(!requireAccess()||!state.player||state.amount<=0||state.amount>state.me.balance)return;show('confirm');const p=state.player;const year=p.created?new Date(p.created).getUTCFullYear():null;$('#dialog-content').innerHTML=`<div class="demo-strip">DEMO · no real Robux transfers</div><div class="confirm-body"><div class="user-card"><img class="avatar" src="${avatar(p.id)}" alt=""><strong>${escapeText(p.displayName)}</strong><div class="handle">@${escapeText(p.name)}</div><div class="user-meta"><span class="row">${icon('user')}Public Roblox profile</span><span class="row">${icon('clock')}${year?'Joined in '+year:'User ID '+p.id}</span></div></div><div class="summary-amount">${icon('robux')}${number(state.amount)}</div><div class="confirm-actions"><button id="send-demo" class="primary">Send demo</button><button id="edit" class="secondary">Edit</button></div><div class="form-error" id="send-error" role="alert"></div><p class="disclosure">This action only creates a demo animation and history entry.<br>No Robux are transferred.</p></div>`;$('#edit').onclick=amountStep;$('#send-demo').onclick=sendDemo;setTimeout(()=>$('#send-demo')?.focus(),60)}
async function sendDemo(){if(!requireAccess()||state.busy)return;const version=state.authRevision;state.busy=true;const b=$('#send-demo');b.disabled=true;$('#edit').disabled=true;$('#close-dialog').disabled=true;b.innerHTML='<span class="button-spinner"></span>Previewing…';$('#send-error').textContent='';state.requestId??=crypto.randomUUID();try{const d=await api('/api/demo-gifts',{recipient_id:state.player.id,amount:state.amount,request_id:state.requestId});if(version!==state.authRevision||!requireAccess())return;updateBalance(d.gift.balance_after);state.busy=false;closeDialog();toast(`DEMO completed · ${number(d.gift.amount)} to @${d.gift.recipient_name} · no Robux sent`);confetti();try{tg?.HapticFeedback?.notificationOccurred('success')}catch(e){}state.requestId=null}catch(e){state.busy=false;if($('#send-error')){$('#send-error').textContent=e.message;b.disabled=false;$('#edit').disabled=false;$('#close-dialog').disabled=false;b.textContent='Retry demo'}}}
function confetti(){if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;for(let i=0;i<22;i++){const p=document.createElement('i');p.className='confetti';p.style.background=['#5f80ff','#a3b5ff','#f3ce7e','#ffffff'][i%4];p.style.setProperty('--dx',(Math.random()*440-220)+'px');p.style.setProperty('--dy',(Math.random()*280-140)+'px');p.style.setProperty('--rot',(Math.random()*550)+'deg');document.body.appendChild(p);setTimeout(()=>p.remove(),900)}}
async function history(){if(!requireAccess())return;state.lastFocus=document.activeElement;show('history','Demo history');$('#dialog-content').innerHTML='<div class="history-list"><div class="skeleton"></div><div class="skeleton"></div></div>';try{const d=await api('/api/history');if(state.step!=='history')return;$('#dialog-content').innerHTML=`<div class="demo-strip">All entries below are demonstrations</div><div class="history-list">${d.gifts.length?d.gifts.map(g=>`<div class="history-item"><img class="avatar" src="${avatar(g.recipient_id)}" alt=""><div class="grow"><strong>@${escapeText(g.recipient_name)}</strong><small>${new Date(g.created_at*1000).toLocaleString()} · DEMO</small></div><div class="history-amount">${icon('robux')} ${number(g.amount)}</div></div>`).join(''):'<div class="empty">No demos yet.<br>Choose a player to preview the flow.</div>'}</div>`}catch(e){if(state.step==='history')$('#dialog-content').innerHTML=`<div class="empty">${escapeText(e.message)}</div>`}}
$('#history-top').onclick=history;
$('#about-side').onclick=()=>{show('about','About Gifter');$('#dialog-content').innerHTML=`<div class="info-body">Independent recreation of a reference interface.<br><br><b>Gifter does not transfer Robux.</b> Profile search and avatars use public Roblox APIs. You never need a Roblox password or session cookie here.<br><br>Telegram Stars purchase access to this demo only. For payment support, use <b>/paysupport</b> in the bot.<br><br>Real gifting must be completed on <a href="https://www.roblox.com/upgrades/robux" target="_blank" rel="noopener">the official Roblox website</a>.</div>`};
(async()=>{try{state.config=await api('/api/config');if(state.config.preview)$('#preview-note').hidden=false;if(state.config.bot){$('#buy-link').href=`https://t.me/${state.config.bot}?start=stars`;$('#buy-link').target='_blank';$('#buy-link').rel='noopener'}try{await loadMe();return}catch(e){}if(tg?.initData){try{state.authRevision++;const session=await api('/api/telegram',{init_data:tg.initData});state.token=session.session_token;await loadMe()}catch(e){setLoginError(e.message)}}}catch(e){setLoginError(e.message)}})();
async function refreshAccess(){updateExpiry();if(state.me){try{await loadMe()}catch(e){}}}
setInterval(updateExpiry,1000);setInterval(refreshAccess,15000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)refreshAccess()});
window.addEventListener('pageshow',refreshAccess);window.addEventListener('focus',refreshAccess);
</script></body></html>'''


def run_self_tests():
    from concurrent.futures import ThreadPoolExecutor
    from urllib.parse import urlencode
    from unittest.mock import patch

    class BillingTests(unittest.TestCase):
        def setUp(self):
            self.temp = tempfile.TemporaryDirectory()
            self.cfg = Config(secret="test-secret-" * 5, sqlite_path=self.temp.name + "/db.sqlite3", public_url="https://example.test", owners=(999,))
            self.db = Database(self.cfg)
            self.store = Store(self.cfg, self.db)

        def tearDown(self):
            self.db.close()
            self.temp.cleanup()

        def order(self, plan="1h", uid=42):
            return self.db.run_sync(lambda tx: self.store.order(tx, uid, plan))

        def payment(self, order):
            return {"invoice_payload": order["id"], "currency": "XTR", "total_amount": order["stars"], "telegram_payment_charge_id": "charge-" + order["id"]}

        def buy(self, plan="1h", uid=42):
            order = self.order(plan, uid)
            self.db.run_sync(lambda tx: self.store.paid(tx, uid, self.payment(order)))
            return order, key_for(order["id"], self.cfg.secret)

        def test_exact_prices(self):
            self.assertEqual([(p["stars"], p["seconds"]) for p in PLANS.values()],
                [(5, 3600), (15, 7200), (30, 86400), (50, 172800), (100, 432000), (400, None)])

        def test_precheck_validates_user_currency_amount_and_expiry(self):
            order = self.order()
            q = {**self.payment(order), "from": {"id": 42}}
            self.assertIsNone(self.db.run_sync(lambda tx: self.store.precheck(tx, q)))
            for override in ({"from": {"id": 666}}, {"total_amount": 1}, {"currency": "USD"}, {"invoice_payload": "unknown"}):
                self.assertIsNotNone(self.db.run_sync(lambda tx: self.store.precheck(tx, {**q, **override})))
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT COUNT(*) AS n FROM licenses"))["n"], 0)
            self.db.run_sync(lambda tx: tx.execute("UPDATE orders SET created_at=?", (now() - 3601,)))
            self.assertIsNotNone(self.db.run_sync(lambda tx: self.store.precheck(tx, q)))

        def test_payment_replay_issues_one_key_and_receipt(self):
            order = self.order()
            with ThreadPoolExecutor(max_workers=6) as executor:
                results = list(executor.map(lambda _: self.db.run_sync(lambda tx: self.store.paid(tx, 42, self.payment(order))), range(12)))
            self.assertTrue(all(x == order["id"] for x in results))
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT COUNT(*) AS n FROM licenses"))["n"], 1)
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT COUNT(*) AS n FROM outbox WHERE id LIKE 'receipt:%'"))["n"], 1)

        def test_wrong_payment_never_grants_license(self):
            order = self.order()
            self.db.run_sync(lambda tx: self.store.paid(tx, 42, {**self.payment(order), "total_amount": 4}))
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT COUNT(*) AS n FROM licenses"))["n"], 0)
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT COUNT(*) AS n FROM payment_incidents"))["n"], 1)

        def test_expiry_starts_at_activation_and_never_resets(self):
            _, key = self.buy()
            row = self.db.run_sync(lambda tx: tx.one("SELECT * FROM licenses"))
            self.assertIsNone(row["activated_at"])
            token, _ = self.db.run_sync(lambda tx: self.store.activate(tx, key, clock=10000))
            self.db.run_sync(lambda tx: self.store.activate(tx, key, clock=10100))
            row = self.db.run_sync(lambda tx: tx.one("SELECT * FROM licenses"))
            self.assertEqual((row["activated_at"], row["expires_at"]), (10000, 13600))
            self.assertIsNotNone(self.db.run_sync(lambda tx: self.store.session(tx, token, clock=13599)))
            self.assertIsNone(self.db.run_sync(lambda tx: self.store.session(tx, token, clock=13600)))
            with self.assertRaises(ValueError):
                self.db.run_sync(lambda tx: self.store.activate(tx, key, clock=13600))

        def test_forever_and_refund_revoke_existing_sessions(self):
            order, key = self.buy("forever")
            token, _ = self.db.run_sync(lambda tx: self.store.activate(tx, key))
            self.assertIsNone(self.db.run_sync(lambda tx: self.store.session(tx, token))["expires_at"])
            self.db.run_sync(lambda tx: self.store.refunded(tx, self.payment(order)["telegram_payment_charge_id"]))
            self.assertIsNone(self.db.run_sync(lambda tx: self.store.session(tx, token)))
            with self.assertRaises(ValueError):
                self.db.run_sync(lambda tx: self.store.activate(tx, key))

        def test_refund_only_affects_that_purchase(self):
            first, key1 = self.buy("forever")
            _, key2 = self.buy("2d")
            token2, _ = self.db.run_sync(lambda tx: self.store.activate(tx, key2))
            self.db.run_sync(lambda tx: self.store.refunded(tx, self.payment(first)["telegram_payment_charge_id"]))
            self.assertIsNotNone(self.db.run_sync(lambda tx: self.store.session(tx, token2)))

        def test_gift_retry_debits_only_once(self):
            _, key = self.buy()
            token, _ = self.db.run_sync(lambda tx: self.store.activate(tx, key))
            gift = lambda tx: self.store.gift(tx, token, 1, "Roblox", 100, "request-123456789")
            a, b = self.db.run_sync(gift), self.db.run_sync(gift)
            self.assertEqual(a["id"], b["id"])
            self.assertEqual(b["balance_after"], DEMO_BALANCE - 100)
            with self.assertRaises(ValueError):
                self.db.run_sync(lambda tx: self.store.gift(tx, token, 1, "Roblox", 101, "request-123456789"))

        def test_concurrent_gifts_cannot_overdraw(self):
            _, key = self.buy()
            token, _ = self.db.run_sync(lambda tx: self.store.activate(tx, key))
            def give(n):
                try:
                    return self.db.run_sync(lambda tx: self.store.gift(tx, token, 1, "Roblox", 600000, "request-number-" + str(n)))
                except ValueError:
                    return None
            with ThreadPoolExecutor(max_workers=2) as executor:
                results = list(executor.map(give, [1, 2]))
            self.assertEqual(sum(x is not None for x in results), 1)
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT balance FROM wallets WHERE owner_id=42"))["balance"], 400000)

        def test_invalid_amount_rolls_back(self):
            _, key = self.buy()
            token, _ = self.db.run_sync(lambda tx: self.store.activate(tx, key))
            for amount in (0, -1, 1.5, True, DEMO_BALANCE + 1):
                with self.assertRaises(ValueError):
                    self.db.run_sync(lambda tx: self.store.gift(tx, token, 1, "Roblox", amount, "x" * 20))
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT balance FROM wallets WHERE owner_id=42"))["balance"], DEMO_BALANCE)

        def test_restart_preserves_paid_key(self):
            _, key = self.buy()
            self.db.close()
            self.db = Database(self.cfg)
            self.store = Store(self.cfg, self.db)
            token, _ = self.db.run_sync(lambda tx: self.store.activate(tx, key))
            self.assertEqual(self.db.run_sync(lambda tx: self.store.session(tx, token))["owner_id"], 42)

        def test_telegram_signature_rejects_tampering_replay_and_duplicates(self):
            token = "12345:example"
            fields = {"auth_date": "10000", "user": '{"id":42}', "query_id": "AA-test"}
            def sign(data):
                secret = hmac.digest(b"WebAppData", token.encode(), "sha256")
                check = "\n".join(f"{k}={data[k]}" for k in sorted(data))
                return urlencode({**data, "hash": hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()})
            raw = sign(fields)
            self.assertEqual(verify_init_data(raw, token, clock=10000)["id"], 42)
            for invalid, clock in ((raw.replace('42', '43'), 10000), (raw, 14000), (raw, 9900), (raw + "&auth_date=10000", 10000)):
                with self.assertRaises(ValueError):
                    verify_init_data(invalid, token, clock=clock)

        def test_admin_id_env_and_legacy_owners(self):
            with patch.dict(os.environ, {"ADMIN_ID": "123456789", "BOT_TOKEN": "123456:test_token", "APP_SECRET": "s" * 48,
                                         "PUBLIC_URL": "https://example.test"}, clear=True):
                cfg = Config.from_env()
                cfg.validate()
                self.assertEqual(cfg.admin_ids, (123456789,))
                os.environ["OWNER_IDS"] = "55,123456789"
                self.assertEqual(Config.from_env().admin_ids, (123456789, 55))

        def test_grants_require_admin_and_retries_issue_one_key(self):
            with self.assertRaises(PermissionError):
                self.db.run_sync(lambda tx: self.store.grant(tx, 42, 42, "lifetime", "untrusted"))
            self.cfg.owners, self.cfg.admin_id = (), 999
            for duration, seconds in (("1m", 60), ("1h", 3600), ("1d", 86400), ("1w", 604800), ("lifetime", None)):
                a = self.db.run_sync(lambda tx: self.store.grant(tx, 999, 42, duration, duration))
                b = self.db.run_sync(lambda tx: self.store.grant(tx, 999, 42, duration, duration))
                self.assertEqual(a["id"], b["id"])
                self.assertEqual((a["stars"], a["status"], a["duration"]), (0, "granted", seconds))
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT COUNT(*) n FROM licenses"))["n"], 5)
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT COUNT(*) n FROM license_grants WHERE admin_id=999"))["n"], 5)

        def test_minute_grant_expires_exactly_and_lifetime_has_no_deadline(self):
            order = self.db.run_sync(lambda tx: self.store.grant(tx, 999, 42, "1m", "minute"))
            key = key_for(order["id"], self.cfg.secret)
            token, expiry = self.db.run_sync(lambda tx: self.store.activate(tx, key, clock=1000))
            self.assertEqual(expiry, 1060)
            self.assertIsNotNone(self.db.run_sync(lambda tx: self.store.session(tx, token, clock=1059)))
            self.assertIsNone(self.db.run_sync(lambda tx: self.store.session(tx, token, clock=1060)))
            with self.assertRaises(ValueError):
                self.db.run_sync(lambda tx: self.store.activate(tx, key, clock=1060))
            order = self.db.run_sync(lambda tx: self.store.grant(tx, 999, 42, "lifetime", "forever-grant"))
            token, _ = self.db.run_sync(lambda tx: self.store.activate(tx, key_for(order["id"], self.cfg.secret)))
            self.assertIsNone(self.db.run_sync(lambda tx: self.store.session(tx, token))["expires_at"])

        def test_profile_only_commits_on_save_and_survives_restart(self):
            self.buy()
            draft = self.db.run_sync(lambda tx: self.store.open_profile(tx, 42, "form"))
            self.db.run_sync(lambda tx: self.store.await_profile_field(tx, 42, draft["draft_id"], "balance"))
            self.db.run_sync(lambda tx: self.store.edit_profile(tx, 42, "9 999 999 999", "balance-edit"))
            self.db.run_sync(lambda tx: self.store.await_profile_field(tx, 42, draft["draft_id"], "nickname"))
            self.db.run_sync(lambda tx: self.store.edit_profile(tx, 42, "Player_42", "name-edit"))
            self.assertEqual(self.db.run_sync(lambda tx: self.store.profile(tx, 42)), {"balance": DEMO_BALANCE, "nickname": DEFAULT_NICKNAME})
            data = self.db.run_sync(lambda tx: self.store.save_profile(tx, 42, draft["draft_id"], "save"))
            self.assertEqual(data, {"balance": MAX_DEMO_BALANCE, "nickname": "Player_42"})
            self.assertIsNone(self.db.run_sync(lambda tx: tx.one("SELECT activated_at FROM licenses WHERE owner_id=42"))["activated_at"])
            self.db.close()
            self.db = Database(self.cfg)
            self.store = Store(self.cfg, self.db)
            self.assertEqual(self.db.run_sync(lambda tx: self.store.profile(tx, 42)), data)

        def test_profile_rejects_wrong_owner_and_expired_key_at_save(self):
            order, key = self.buy()
            self.db.run_sync(lambda tx: self.store.activate(tx, key))
            draft = self.db.run_sync(lambda tx: self.store.open_profile(tx, 42, "form"))
            with self.assertRaises(ValueError):
                self.db.run_sync(lambda tx: self.store.open_profile(tx, 666, "unlicensed"))
            with self.assertRaises(ValueError):
                self.db.run_sync(lambda tx: self.store.save_profile(tx, 666, draft["draft_id"], "wrong-user"))
            self.db.run_sync(lambda tx: tx.execute("UPDATE licenses SET expires_at=? WHERE order_id=?", (now(), order["id"])))
            with self.assertRaises(ValueError):
                self.db.run_sync(lambda tx: self.store.save_profile(tx, 42, draft["draft_id"], "expired"))
            self.assertIsNone(self.db.run_sync(lambda tx: self.store.available_license(tx, 42)))

        def test_nickname_edit_does_not_restore_spent_balance_and_save_replay_is_safe(self):
            _, key = self.buy()
            token, _ = self.db.run_sync(lambda tx: self.store.activate(tx, key))
            draft = self.db.run_sync(lambda tx: self.store.open_profile(tx, 42, "form"))
            self.db.run_sync(lambda tx: self.store.await_profile_field(tx, 42, draft["draft_id"], "nickname"))
            self.db.run_sync(lambda tx: self.store.edit_profile(tx, 42, "NewName", "edit"))
            self.db.run_sync(lambda tx: self.store.gift(tx, token, 1, "Roblox", 100, "before-save"))
            self.db.run_sync(lambda tx: self.store.save_profile(tx, 42, draft["draft_id"], "save"))
            self.db.run_sync(lambda tx: self.store.gift(tx, token, 1, "Roblox", 200, "after-save"))
            self.db.run_sync(lambda tx: self.store.save_profile(tx, 42, draft["draft_id"], "save"))
            with self.assertRaises(ValueError):
                self.db.run_sync(lambda tx: self.store.save_profile(tx, 42, draft["draft_id"], "new-callback-old-form"))
            self.assertEqual(self.db.run_sync(lambda tx: self.store.profile(tx, 42))["balance"], DEMO_BALANCE - 300)

        def test_settings_validation_and_expired_draft(self):
            for value in ("-1", "1.5", "10000000000", "<b>100</b>", ""):
                with self.assertRaises(ValueError):
                    validate_demo_balance(value)
            for value in ("", "A" * 33, "name\nother", "name\u202eother"):
                with self.assertRaises(ValueError):
                    validate_nickname(value)
            for value in ("0m", "-1h", "1s", "forever", "999999w", "1h 2d"):
                with self.assertRaises(ValueError):
                    grant_duration(value)
            self.buy()
            draft = self.db.run_sync(lambda tx: self.store.open_profile(tx, 42, "draft"))
            self.db.run_sync(lambda tx: tx.execute("UPDATE profile_drafts SET expires_at=?", (now(),)))
            with self.assertRaises(ValueError):
                self.db.run_sync(lambda tx: self.store.save_profile(tx, 42, draft["draft_id"], "stale"))

    class BotFlowTests(unittest.IsolatedAsyncioTestCase):
        async def asyncSetUp(self):
            self.temp = tempfile.TemporaryDirectory()
            self.cfg = Config(admin_id=999, group_id=-100123, secret="s" * 48,
                              public_url="https://example.test", sqlite_path=self.temp.name + "/bot.sqlite3")
            self.db = Database(self.cfg)
            self.svc = Service(self.cfg, self.db)
            class FakeTelegram:
                id, username = 777, "test_gifter_bot"
                async def call(self, *args, **kwargs):
                    return True
            self.svc.tg = FakeTelegram()
            self.seq = 0

        async def asyncTearDown(self):
            self.db.close()
            self.temp.cleanup()

        async def message(self, uid, text, chat=None, reply=None):
            self.seq += 1
            msg = {"message_id": self.seq, "from": {"id": uid, "is_bot": False},
                   "chat": chat or {"id": uid, "type": "private"}, "text": text}
            if reply:
                msg["reply_to_message"] = {"from": {"id": reply, "is_bot": False}}
            update = {"update_id": self.seq, "message": msg}
            await self.svc.process(update)
            return update

        async def callback(self, uid, data):
            self.seq += 1
            await self.svc.process({"update_id": self.seq, "callback_query": {"id": str(self.seq),
                "from": {"id": uid}, "data": data, "message": {"chat": {"id": uid, "type": "private"}}}})

        def messages(self):
            return [json.loads(r["payload"]) for r in self.db.run_sync(lambda tx: tx.all("SELECT payload FROM outbox"))]

        async def test_private_grant_authorization_and_duplicate_update(self):
            await self.message(42, "/give lifetime")
            self.assertEqual(self.db.run_sync(lambda tx: tx.one("SELECT COUNT(*) n FROM licenses"))["n"], 0)
            update = await self.message(999, "/give 1m 42")
            await self.svc.process(update)
            rows = self.db.run_sync(lambda tx: tx.all("SELECT * FROM licenses"))
            self.assertEqual(len(rows), 1)
            self.assertEqual((rows[0]["owner_id"], rows[0]["duration"]), (42, 60))
            await self.message(42, "/key")
            self.assertTrue(any("выдан админом" in p["text"] for p in self.messages()))

        async def test_group_reply_grant_never_publishes_keys_in_group(self):
            await self.message(999, "/give 1w", {"id": -100123, "type": "supergroup"}, reply=42)
            row = self.db.run_sync(lambda tx: tx.one("SELECT * FROM licenses"))
            self.assertEqual((row["owner_id"], row["duration"]), (42, 604800))
            self.assertTrue(all(p["chat_id"] in (999, 42) for p in self.messages()))

        async def test_start_settings_save_cancel_and_html_escape(self):
            await self.message(999, "/give lifetime 42")
            await self.message(42, "/start")
            self.assertTrue(any(b.get("callback_data") == "profile" for p in self.messages()
                                for row in p.get("reply_markup", {}).get("inline_keyboard", []) for b in row))
            await self.callback(42, "profile")
            draft = self.db.run_sync(lambda tx: tx.one("SELECT * FROM profile_drafts WHERE user_id=42"))
            await self.callback(42, "profile:balance:" + draft["draft_id"])
            await self.message(42, "123456789")
            await self.callback(42, "profile:nickname:" + draft["draft_id"])
            await self.message(42, "<Player&42>")
            self.assertEqual(self.db.run_sync(lambda tx: self.svc.store.profile(tx, 42))["balance"], DEMO_BALANCE)
            await self.callback(42, "profile:save:" + draft["draft_id"])
            self.assertEqual(self.db.run_sync(lambda tx: self.svc.store.profile(tx, 42)), {"balance": 123456789, "nickname": "<Player&42>"})
            self.assertTrue(any("&lt;Player&amp;42&gt;" in p["text"] for p in self.messages()))
            await self.message(42, "/settings")
            await self.message(42, "/cancel")
            self.assertIsNone(self.db.run_sync(lambda tx: tx.one("SELECT * FROM profile_drafts WHERE user_id=42")))

    class HTTPTests(unittest.IsolatedAsyncioTestCase):
        async def asyncSetUp(self):
            from aiohttp import CookieJar
            from aiohttp.test_utils import TestClient, TestServer
            self.temp = tempfile.TemporaryDirectory()
            self.cfg = Config(preview=True, secret="s" * 48, sqlite_path=self.temp.name + "/http.sqlite3")
            self.app = make_app(self.cfg)
            self.client = TestClient(TestServer(self.app), cookie_jar=CookieJar(unsafe=True))
            await self.client.start_server()
            self.origin = str(self.client.make_url("/")).rstrip("/")

        async def asyncTearDown(self):
            await self.client.close()
            self.temp.cleanup()

        async def test_http_cookie_auth_and_csrf(self):
            self.assertEqual((await self.client.get('/api/me')).status, 401)
            self.assertEqual((await self.client.post('/api/activate', json={"key": "DEMO-LOCAL"})).status, 403)
            response = await self.client.post('/api/activate', headers={"Origin": self.origin}, json={"key": "DEMO-LOCAL"})
            self.assertEqual(response.status, 200)
            self.assertTrue(response.cookies['gifter_session']['httponly'])
            self.assertEqual(response.cookies['gifter_session']['samesite'], 'Strict')
            me = await self.client.get('/api/me')
            self.assertEqual((await me.json())['balance'], DEMO_BALANCE)
            await self.client.post('/api/logout', headers={"Origin": self.origin}, json={})
            self.assertEqual((await self.client.get('/api/me')).status, 401)

        async def test_webhook_secret_inbox_dedup_and_inline_precheckout(self):
            self.cfg.preview = False
            svc = self.app['svc']
            row = await svc.db.run(lambda tx: svc.store.order(tx, 42, '1d'))
            update = {"update_id": 100, "pre_checkout_query": {"id": "pre-1", "from": {"id": 42}, "currency": "XTR", "total_amount": 30, "invoice_payload": row['id']}}
            self.assertEqual((await self.client.post('/telegram/webhook', json=update)).status, 403)
            headers = {"X-Telegram-Bot-Api-Secret-Token": self.cfg.webhook_secret}
            result = await self.client.post('/telegram/webhook', headers=headers, json=update)
            self.assertEqual(await result.json(), {"method": "answerPreCheckoutQuery", "pre_checkout_query_id": "pre-1", "ok": True})
            update = {"update_id": 101, "message": {"message_id": 4, "from": {"id": 42}, "chat": {"id": 42, "type": "private"}, "successful_payment": {"currency": "XTR", "total_amount": 30, "invoice_payload": row['id'], "telegram_payment_charge_id": "test-http-charge"}}}
            for _ in range(2):
                self.assertEqual((await self.client.post('/telegram/webhook', headers=headers, json=update)).status, 200)
            self.assertEqual((await svc.db.run(lambda tx: tx.one("SELECT COUNT(*) AS n FROM inbox")))['n'], 1)
            await svc.process(update)
            self.assertEqual((await svc.db.run(lambda tx: tx.one("SELECT COUNT(*) AS n FROM licenses WHERE owner_id=42")))['n'], 1)

        async def test_telegram_web_bearer_without_cookies(self):
            response = await self.client.post('/api/activate', headers={"Origin": self.origin}, json={"key": "DEMO-LOCAL"})
            token = (await response.json())["session_token"]
            self.client.session.cookie_jar.clear()
            headers = {"Authorization": "Bearer " + token}
            self.assertEqual((await self.client.get('/api/me', headers=headers)).status, 200)
            await self.client.post('/api/logout', headers={**headers, "Origin": self.origin}, json={})
            self.assertEqual((await self.client.get('/api/me', headers=headers)).status, 401)

        async def test_saved_profile_me_and_all_protected_routes_reject_expired_key(self):
            response = await self.client.post('/api/activate', headers={"Origin": self.origin}, json={"key": "DEMO-LOCAL"})
            token = (await response.json())["session_token"]
            svc = self.app["svc"]
            draft = await svc.db.run(lambda tx: svc.store.open_profile(tx, 1, "http-profile"))
            await svc.db.run(lambda tx: svc.store.await_profile_field(tx, 1, draft["draft_id"], "nickname"))
            await svc.db.run(lambda tx: svc.store.edit_profile(tx, 1, "TestPlayer", "http-name"))
            await svc.db.run(lambda tx: svc.store.save_profile(tx, 1, draft["draft_id"], "http-save"))
            me = await (await self.client.get('/api/me')).json()
            self.assertEqual(me["nickname"], "TestPlayer")
            self.assertGreater(me["session_expires_at"], me["server_time"])
            await svc.db.run(lambda tx: tx.execute("UPDATE licenses SET duration=60,expires_at=? WHERE owner_id=1", (now(),)))
            for path in ("/api/me", "/api/users?q=Roblox", "/api/user/1", "/api/avatar/1", "/api/history"):
                self.assertEqual((await self.client.get(path, headers={"Authorization": "Bearer " + token})).status, 401, path)
            response = await self.client.post('/api/demo-gifts', headers={"Origin": self.origin}, json={})
            self.assertEqual(response.status, 401)

    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(BillingTests),
                               unittest.defaultTestLoader.loadTestsFromTestCase(BotFlowTests),
                               unittest.defaultTestLoader.loadTestsFromTestCase(HTTPTests)])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(description="Gifter — one-file Telegram Stars bot and visual demo")
    parser.add_argument("--preview", action="store_true", help="Local-only preview; no Telegram network calls")
    parser.add_argument("--self-test", action="store_true", help="Run payment, session and HTTP tests without external APIs")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    if args.self_test:
        raise SystemExit(run_self_tests())
    temporary = None
    try:
        cfg = Config.from_env(args.preview)
        if args.preview:
            temporary = tempfile.TemporaryDirectory(prefix="gifter-preview-")
            cfg.sqlite_path, cfg.database_url = temporary.name + "/preview.sqlite3", ""
            cfg.secret, cfg.token = secrets.token_hex(32), ""
            cfg.public_url = f"http://127.0.0.1:{cfg.port}"
            LOG.info("Preview: http://127.0.0.1:%s — key DEMO-LOCAL (no real payments)", cfg.port)
        app = make_app(cfg)
        web.run_app(app, host="127.0.0.1" if cfg.preview else "0.0.0.0", port=cfg.port,
                    access_log=None, print=None, shutdown_timeout=20)
    except (ValueError, ImportError) as exc:
        raise SystemExit(str(exc)) from None
    finally:
        if temporary:
            temporary.cleanup()


if __name__ == "__main__":
    main()
