"""
ADVANCED OOP
  1. Custom exceptions (extending Exception)
  2. Mixins
  3. Composition patterns (strategy / dependency injection)
  4. __slots__

(Iterators, generators, dunder methods and @property are already in
python_oop_complete.py, sections 2, 4, 10 and 11.)
"""
import json
import tracemalloc


def heading(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


# ============================================================
# 1. CUSTOM EXCEPTIONS
# ============================================================
heading("1. CUSTOM EXCEPTIONS")

# Why? Built-in errors (ValueError, KeyError...) are generic. A custom exception
# says exactly WHAT went wrong in YOUR program, and lets callers catch just that.

# Step 1: one BASE exception for the whole project.
# Catching ScannerError later catches every error our scanner can raise.
class ScannerError(Exception):
    """Base class for all scanner errors."""
    # An empty body is enough: we inherit everything from Exception.


# Step 2: specific exceptions inherit from the base.
class InvalidPortError(ScannerError):
    def __init__(self, port):
        self.port = port                                   # keep extra data on the exception
        # super().__init__(message) sets the text shown by str(e) / tracebacks
        super().__init__(f"Port {port!r} is invalid (must be an int 1-65535)")


class TargetUnreachableError(ScannerError):
    def __init__(self, host, reason="timeout"):
        self.host = host
        self.reason = reason
        super().__init__(f"Cannot reach {host}: {reason}")


def check_port(port):
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise InvalidPortError(port)                       # 'raise' throws the exception
    return port


def connect(host):
    if host.endswith(".invalid"):
        raise TargetUnreachableError(host, "DNS failure")
    return f"connected to {host}"


# Catch the most specific exception first, then the base class as a safety net.
for port in (80, 70000, "http"):
    try:
        print("OK:", check_port(port))
    except InvalidPortError as e:
        print("Invalid port ->", e, "| stored value:", e.port)

try:
    connect("nothing.invalid")
except InvalidPortError:
    print("not this one")
except ScannerError as e:                                  # catches ANY ScannerError child
    print("Scanner problem ->", e, "| host:", e.host, "| reason:", e.reason)

print(issubclass(InvalidPortError, ScannerError))          # True
print(issubclass(ScannerError, Exception))                 # True


# ============================================================
# 2. MIXINS
# ============================================================
heading("2. MIXINS")

# A mixin is a small class that adds ONE ability and is not meant to be used alone.
# You combine (mix in) several of them into a class via multiple inheritance.
# Rules of thumb: no __init__ in a mixin, no state of its own, name it ...Mixin.

class JsonMixin:
    """Adds .to_json() to any class that stores its data in __dict__."""
    def to_json(self):
        return json.dumps(self.__dict__, indent=2, default=str)


class LogMixin:
    """Adds .log() to any class."""
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")


class BaseScanner:
    def __init__(self, target):
        self.target = target

    def scan(self):
        raise NotImplementedError("Subclasses must implement scan()")


# Mixins go on the LEFT, the real base class goes LAST.
class PortScanner(LogMixin, JsonMixin, BaseScanner):
    def __init__(self, target, ports):
        super().__init__(target)       # mixins have no __init__, so this reaches BaseScanner
        self.ports = ports
        self.results = {}

    def scan(self):
        self.log(f"scanning {self.target}")               # ability from LogMixin
        self.results = {p: ("open" if p in (22, 80) else "closed") for p in self.ports}
        return self.results


scanner = PortScanner("10.0.0.5", [22, 80, 443])
scanner.scan()
print(scanner.to_json())                                   # ability from JsonMixin
print([c.__name__ for c in PortScanner.__mro__])           # search order for methods

# The same mixin can be reused by completely unrelated classes:
class Report(JsonMixin):
    def __init__(self, title):
        self.title = title

print(Report("Weekly scan").to_json())


# ============================================================
# 3. COMPOSITION PATTERNS (HAS-A, strategy / dependency injection)
# ============================================================
heading("3. COMPOSITION PATTERNS")

# "Favor composition over inheritance": instead of making 5 subclasses
# (ConsoleScanner, JsonScanner, ...), give the scanner a swappable PART.
# Any object with a .report(results) method works (duck typing).

class ConsoleReporter:
    def report(self, results):
        for port, state in results.items():
            print(f"  port {port}: {state}")


class JsonReporter:
    def report(self, results):
        print(json.dumps(results))


class QuietReporter:
    def report(self, results):
        open_ports = [p for p, s in results.items() if s == "open"]
        print("  open ports:", open_ports)


class Scanner:
    # The reporter is INJECTED from outside (dependency injection).
    def __init__(self, target, reporter):
        self.target = target
        self.reporter = reporter                           # HAS-A reporter

    def run(self, ports):
        results = {p: ("open" if p % 2 == 0 else "closed") for p in ports}
        self.reporter.report(results)                      # delegate the work


for reporter in (ConsoleReporter(), JsonReporter(), QuietReporter()):
    print(type(reporter).__name__)
    Scanner("10.0.0.5", reporter).run([20, 21, 22])

# Behaviour can even be swapped at runtime:
s = Scanner("10.0.0.5", ConsoleReporter())
s.reporter = QuietReporter()
s.run([80, 81])


# ============================================================
# 4. __slots__  (memory optimisation)
# ============================================================
heading("4. __slots__")

# Normally every object has a __dict__ (a dictionary) to store its attributes:
# flexible, but it costs memory. __slots__ replaces that dict with a fixed,
# compact layout.

class PointDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PointSlots:
    __slots__ = ("x", "y")                                 # only these attributes are allowed

    def __init__(self, x, y):
        self.x = x
        self.y = y


p1 = PointDict(1, 2)
p2 = PointSlots(1, 2)

print("PointDict  has __dict__:", hasattr(p1, "__dict__"))     # True
print("PointSlots has __dict__:", hasattr(p2, "__dict__"))     # False

p1.z = 3                                                   # fine: dicts accept anything
try:
    p2.z = 3                                               # not in __slots__
except AttributeError as e:
    print("Error:", e)


def memory_used(cls, n=100_000):
    tracemalloc.start()
    objects = [cls(i, i) for i in range(n)]                # keep them alive while measuring
    current, _peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del objects
    return current / 1024

print(f"100k PointDict : {memory_used(PointDict):,.0f} KB")
print(f"100k PointSlots: {memory_used(PointSlots):,.0f} KB   <- noticeably smaller")

# Things to remember (common interview points):
#   * Attributes not listed in __slots__ can't be added (typo-safe, but less flexible).
#   * A subclass that does NOT define its own __slots__ gets a __dict__ again.
#   * No __weakref__ unless you add "__weakref__" to __slots__.
#   * Worth it only when you create MANY small objects.
class Point3D(PointSlots):
    __slots__ = ("z",)                                     # extend slots in the child

p3 = Point3D(1, 2)
p3.z = 3
print(p3.x, p3.y, p3.z)



"""
ERROR HANDLING & ROBUSTNESS
  7. Multiple except blocks, else / finally, exception chaining
  8. Context managers (with statement, __enter__ / __exit__)
  9. logging module
"""
import json
import logging
import os
import tempfile
import time
from contextlib import contextmanager, suppress


def heading(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


# ============================================================
# 7a. MULTIPLE EXCEPT BLOCKS
# ============================================================
heading("7a. MULTIPLE EXCEPT BLOCKS")

def average_per_port(text):
    try:
        data = json.loads(text)          # may raise json.JSONDecodeError
        port = int(data["port"])         # may raise KeyError, ValueError, TypeError
        value = 100 / port               # may raise ZeroDivisionError
    # Python checks the except blocks TOP to BOTTOM and runs the FIRST match.
    # So: most specific first, general (Exception) last.
    except json.JSONDecodeError as e:
        print("  bad JSON:", e.msg)
    except KeyError as e:
        print("  missing key:", e)
    except (ValueError, TypeError) as e:          # one block for several exception types
        print("  bad port value:", type(e).__name__, "-", e)
    except ZeroDivisionError:
        print("  port cannot be 0")
    except Exception as e:                        # last-resort safety net
        print("  unexpected:", repr(e))
    else:
        # runs ONLY if the try block finished with no exception
        print("  ok ->", value)
        return value
    finally:
        # ALWAYS runs: success, handled error, or even a return above.
        # Best place for cleanup (close files, sockets, connections).
        print("  (finally: cleanup runs every time)")


for sample in ('{"port": 80}', "not json", "{}", '{"port": "abc"}',
               '{"port": 0}', '{"port": null}'):
    print("input:", sample)
    average_per_port(sample)

# Never write a bare `except:` - it also swallows Ctrl+C (KeyboardInterrupt)
# and hides bugs. Catch specific exceptions; use `except Exception` only as a net.


# ============================================================
# 7b. EXCEPTION CHAINING
# ============================================================
heading("7b. EXCEPTION CHAINING")

class ConfigError(Exception):
    pass


# (1) EXPLICIT chaining: `raise NewError from original`
# Keeps the low-level cause attached while exposing a friendly high-level error.
def load_port(text):
    try:
        return int(text)
    except ValueError as original:
        raise ConfigError(f"port setting {text!r} is not a number") from original

try:
    load_port("eighty")
except ConfigError as e:
    print("Error      :", e)
    print("__cause__  :", repr(e.__cause__))          # the original ValueError


# (2) IMPLICIT chaining: raising inside an except block WITHOUT 'from'
# Python still records the previous error in __context__.
def implicit():
    try:
        1 / 0
    except ZeroDivisionError:
        raise RuntimeError("cleanup failed")          # new error raised while handling the old one

try:
    implicit()
except RuntimeError as e:
    print("__context__:", repr(e.__context__))        # ZeroDivisionError
    print("__cause__  :", e.__cause__)                # None (not explicit)


# (3) `from None` hides the original (use when it is just noise for the user)
def hide_cause():
    try:
        {}["missing"]
    except KeyError:
        raise ConfigError("setting not found") from None

try:
    hide_cause()
except ConfigError as e:
    print("suppressed context:", e.__suppress_context__)   # True


# (4) Re-raise the same exception after doing something (e.g. logging)
try:
    try:
        int("x")
    except ValueError:
        print("logging the problem, then re-raising...")
        raise                                          # bare raise = same exception again
except ValueError as e:
    print("caught again outside:", e)


# ============================================================
# 8. CONTEXT MANAGERS (with statement)
# ============================================================
heading("8. CONTEXT MANAGERS")

# Full FileOpener walkthrough is in python_oop_complete.py section 11d.
# Here: a practical Timer, three different ways.

# (a) class-based: __enter__ / __exit__
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self                                   # value bound by "as t"

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = time.perf_counter() - self.start
        print(f"  block took {self.elapsed:.2f}s")
        return False                                  # False/None = don't swallow exceptions

with Timer() as t:
    time.sleep(0.1)
print("elapsed attribute:", round(t.elapsed, 1))

# (b) generator-based with @contextmanager (less code)
@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield                                         # the with-block runs here
    finally:                                          # cleanup even if the block raises
        print(f"  {label}: {time.perf_counter() - start:.2f}s")

with timer("sleep test"):
    time.sleep(0.1)

# (c) ready-made: contextlib.suppress ignores the listed exceptions
with suppress(FileNotFoundError):
    os.remove("this_file_does_not_exist.txt")
print("no crash thanks to suppress()")

# Several context managers in ONE with statement:
with tempfile.TemporaryDirectory() as folder, timer("temp dir work"):
    path = os.path.join(folder, "a.txt")
    with open(path, "w") as f:
        f.write("hi")
    print("  wrote", os.path.exists(path))
print("temp dir deleted automatically:", not os.path.exists(folder))


# ============================================================
# 9. LOGGING (replace scattered print() debugging)
# ============================================================
heading("9. LOGGING")

# Why not print()?
#   * levels: filter noise (DEBUG) from problems (ERROR)
#   * timestamps, module names, line numbers for free
#   * send to console AND file (and later syslog, SIEM...) without changing code
#   * switch verbosity on/off in one place

# Levels, low -> high:  DEBUG < INFO < WARNING < ERROR < CRITICAL

# --- Quick setup (fine for small scripts) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logging.info("basicConfig logger works")
logging.debug("hidden: DEBUG is below INFO")

# --- Proper setup for real tools: named logger + handlers ---
log_file = os.path.join(tempfile.gettempdir(), "scanner_demo.log")

logger = logging.getLogger("scanner")        # convention: logging.getLogger(__name__) in modules
logger.setLevel(logging.DEBUG)               # logger level = the minimum it will process
logger.propagate = False                     # don't also send to the root logger (no duplicates)

formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s")

console = logging.StreamHandler()            # -> terminal
console.setLevel(logging.INFO)               # console shows INFO and above
console.setFormatter(formatter)

file_handler = logging.FileHandler(log_file, encoding="utf-8")   # -> file
file_handler.setLevel(logging.DEBUG)         # file keeps everything
file_handler.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file_handler)

logger.debug("only in the file")
logger.info("scan started")
logger.warning("port 8080 responded slowly")
logger.error("connection refused on 10.0.0.9")
logger.critical("scanner crashed")

# Child loggers inherit settings from the parent via dotted names
http_logger = logging.getLogger("scanner.http")
http_logger.info("GET /admin -> 403")

# Log values with % style arguments, not f-strings:
# the string is only built if the message is actually going to be emitted.
host, port = "10.0.0.5", 443
logger.info("checking %s:%d", host, port)

# logger.exception() = ERROR + full traceback. Use inside except blocks.
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("calculation failed")

# Never log secrets (passwords, API keys, tokens).

# Cleanup for this demo: close handlers, show the file, delete it
for h in (console, file_handler):
    h.close()
    logger.removeHandler(h)
with open(log_file, encoding="utf-8") as f:
    print("\n--- first lines of the log FILE (includes DEBUG) ---")
    print("".join(f.readlines()[:3]))
os.remove(log_file)

# For long-running tools use logging.handlers.RotatingFileHandler(
#     "app.log", maxBytes=1_000_000, backupCount=3) so the file never grows forever.



"""
WORKING WITH EXTERNAL DATA
  10. File handling (text, CSV, JSON)
  11. Regular expressions (re)
  12. requests library (HTTP calls, status codes)
  13. Working with APIs (auth headers, query params, pagination)

Setup for section 12-13:   pip install requests
The HTTP demos talk to a tiny server started INSIDE this script, so the whole
file runs offline. The code is identical to what you'd write for a real API.
"""
import csv
import json
import re
import tempfile
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def heading(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


# Everything in sections 10 writes into a throw-away folder
workdir = Path(tempfile.mkdtemp())

# ============================================================
# 10a. FILE HANDLING BASICS
# ============================================================
heading("10a. FILE HANDLING")

notes = workdir / "notes.txt"        # pathlib.Path: works on Windows/Linux/macOS alike

# Modes: "r" read (default) | "w" write (overwrites!) | "a" append | "x" create-only
# Always use `with` (auto-closes the file) and pass encoding="utf-8".
with open(notes, "w", encoding="utf-8") as f:
    f.write("line one\n")
    f.write("line two\n")
    f.writelines(["line three\n", "line four\n"])

with open(notes, "a", encoding="utf-8") as f:        # append keeps existing content
    f.write("line five\n")

with open(notes, encoding="utf-8") as f:
    print("read()    ->", repr(f.read()[:20]), "...")        # whole file as one string

with open(notes, encoding="utf-8") as f:
    print("readline()->", repr(f.readline()))                # one line

with open(notes, encoding="utf-8") as f:
    lines = f.readlines()                                    # list of lines
    print("readlines count:", len(lines))

with open(notes, encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):               # BEST for big files: one line at a time
        print(f"  {number}: {line.rstrip()}")

# pathlib shortcuts
print(notes.read_text(encoding="utf-8").splitlines()[0])
(workdir / "copy.txt").write_text("hello", encoding="utf-8")
print(notes.exists(), notes.suffix, notes.name, notes.parent == workdir)
print(sorted(p.name for p in workdir.glob("*.txt")))         # find files by pattern

try:
    open(workdir / "missing.txt")
except FileNotFoundError as e:
    print("Error:", e.strerror)

# ============================================================
# 10b. CSV
# ============================================================
heading("10b. CSV")

csv_path = workdir / "hosts.csv"
rows = [
    {"host": "10.0.0.1", "port": 22, "state": "open"},
    {"host": "10.0.0.1", "port": 80, "state": "open"},
    {"host": "10.0.0.2", "port": 443, "state": "closed"},
]

# newline="" is REQUIRED with csv (prevents blank lines on Windows)
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["host", "port", "state"])
    writer.writeheader()
    writer.writerows(rows)

# csv.reader -> each row is a LIST
with open(csv_path, newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        print("reader     :", row)

# csv.DictReader -> each row is a DICT keyed by the header (easier, preferred)
with open(csv_path, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print("DictReader :", row["host"], int(row["port"]), row["state"])   # values are strings!

# ============================================================
# 10c. JSON
# ============================================================
heading("10c. JSON")

# Python <-> JSON:  dict<->object, list<->array, str<->string, int/float<->number,
#                   True/False<->true/false, None<->null
data = {"target": "10.0.0.1", "ports": [22, 80], "secure": False, "notes": None,
        "scanned_at": datetime(2026, 9, 28, 10, 30)}

# json.dumps -> string ; json.loads -> from string
text = json.dumps(data, indent=2, sort_keys=True, default=str)   # default=str handles datetime
print(text)
print(json.loads(text)["ports"])

# json.dump / json.load -> straight to/from a FILE object
json_path = workdir / "result.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, default=str)
with open(json_path, encoding="utf-8") as f:
    loaded = json.load(f)
print(type(loaded), loaded["secure"], loaded["notes"])

try:
    json.loads("{bad json}")
except json.JSONDecodeError as e:
    print("JSONDecodeError:", e.msg, "at position", e.pos)

# ============================================================
# 11. REGULAR EXPRESSIONS (re)
# ============================================================
heading("11. REGULAR EXPRESSIONS")

# ALWAYS write patterns as raw strings r"..." so backslashes are left alone.
#
#  .  any char        \d digit        \w word char (letters, digits, _)   \s whitespace
#  \D \W \S = opposites               ^ start   $ end   \b word boundary
#  *  0 or more      +  1 or more     ?  0 or 1         {3}  exactly 3    {2,4} 2 to 4
#  [abc] one of       [^abc] not one of      (a|b) either      (...) group

text = "Server 192.168.1.10 failed, backup is 10.0.0.7. Contact admin@example.com"

# re.search : first match ANYWHERE   |  re.match : must match at the START
# re.fullmatch : the WHOLE string must match (use it for validation)
m = re.search(r"\d{1,3}(?:\.\d{1,3}){3}", text)
print("search    :", m.group(), "at", m.span())
print("match     :", re.match(r"Server", text) is not None, re.match(r"failed", text))
print("fullmatch :", bool(re.fullmatch(r"\d+", "12345")), bool(re.fullmatch(r"\d+", "123a")))

# re.findall : list of ALL matches  |  re.finditer : iterator of match objects
print("findall   :", re.findall(r"\d{1,3}(?:\.\d{1,3}){3}", text))
emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
print("emails    :", emails)

# re.sub : replace  |  re.split : split on a pattern
print("sub       :", re.sub(r"\d{1,3}(?:\.\d{1,3}){3}", "<IP>", text))
print("split     :", re.split(r"[,.]\s*", "a, b. c,d"))

# GROUPS: (...) captures parts, (?P<name>...) gives them names
log_line = '192.168.1.10 - - [28/Sep/2026:10:15:32 +0530] "GET /admin HTTP/1.1" 403 512'
pattern = re.compile(                            # compile once when reused many times
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - - '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<size>\d+)'
)
m = pattern.search(log_line)
print(m.groupdict())
print(m["ip"], m["path"], int(m["status"]))

# FLAGS
print(re.findall(r"error", "Error ERROR error", re.IGNORECASE))       # case-insensitive
print(re.findall(r"^\w+", "one\ntwo\nthree", re.MULTILINE))           # ^ matches each line

# GREEDY vs LAZY: * and + grab as much as possible; add ? to grab as little as possible
html = "<b>bold</b> and <i>italic</i>"
print("greedy:", re.findall(r"<.+>", html))
print("lazy  :", re.findall(r"<.+?>", html))

# Practical: pull every failed status out of many log lines
logs = ['1.1.1.1 "GET /a" 200', '2.2.2.2 "GET /admin" 403', '3.3.3.3 "POST /login" 401']
failed = [re.search(r"^(\S+).* (\d{3})$", l).groups() for l in logs
          if re.search(r" (?:401|403)$", l)]
print("failed:", failed)

# ============================================================
# Local demo server (stands in for a real API in sections 12-13)
# ============================================================
class DemoAPI(BaseHTTPRequestHandler):
    TOKEN = "secret-token"
    ITEMS = list(range(1, 11))          # 10 items to paginate through
    flaky_calls = 0

    def _send(self, code, payload, extra_headers=None):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for key, value in (extra_headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        qs = parse_qs(url.query)
        if url.path == "/items":                                   # needs a Bearer token
            if self.headers.get("Authorization") != f"Bearer {self.TOKEN}":
                return self._send(401, {"error": "unauthorized"})
            page = int(qs.get("page", ["1"])[0])
            per_page = int(qs.get("per_page", ["3"])[0])
            chunk = self.ITEMS[(page - 1) * per_page: page * per_page]
            has_more = page * per_page < len(self.ITEMS)
            return self._send(200, {"items": chunk, "next_page": page + 1 if has_more else None})
        if url.path == "/search":
            return self._send(200, {"query": qs.get("q", [""])[0], "limit": qs.get("limit", ["10"])[0]})
        if url.path == "/flaky":                                    # fails twice, then works
            DemoAPI.flaky_calls += 1
            if DemoAPI.flaky_calls <= 2:
                return self._send(503, {"error": "try later"}, {"Retry-After": "0"})
            return self._send(200, {"ok": True, "attempt": DemoAPI.flaky_calls})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        received = json.loads(self.rfile.read(length) or b"{}")
        self._send(201, {"received": received})

    def log_message(self, *args):                                   # keep the console quiet
        pass


server = HTTPServer(("127.0.0.1", 0), DemoAPI)                      # port 0 = pick a free port
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{server.server_port}"

# ============================================================
# 12. requests LIBRARY
# ============================================================
heading("12. requests LIBRARY")

import requests   # pip install requests

# GET request. ALWAYS pass timeout= (without it a dead server can hang your program forever)
r = requests.get(f"{BASE}/search", timeout=5)
print("status_code :", r.status_code)                # 200
print("ok          :", r.ok)                         # True for status < 400
print("content-type:", r.headers["Content-Type"])    # response headers (case-insensitive dict)
print("text        :", r.text)                        # body as a string
print("json()      :", r.json())                     # body parsed into a dict

# Status codes: 2xx success | 3xx redirect | 4xx YOUR mistake | 5xx SERVER problem
r = requests.get(f"{BASE}/nothing-here", timeout=5)
print(r.status_code, r.ok)                           # 404 False (requests does NOT raise by default)

try:
    r.raise_for_status()                             # turns 4xx/5xx into an exception
except requests.exceptions.HTTPError as e:
    print("HTTPError:", e)

# Network-level failures are different exceptions (no response at all)
try:
    requests.get("http://127.0.0.1:9", timeout=2)    # nothing listens on port 9
except requests.exceptions.ConnectionError:
    print("ConnectionError: could not connect")
except requests.exceptions.Timeout:
    print("Timeout")
# Catch requests.exceptions.RequestException to handle ALL of them at once.

# POST with a JSON body (json= sets the body AND Content-Type: application/json)
r = requests.post(f"{BASE}/echo", json={"user": "robi", "role": "admin"}, timeout=5)
print(r.status_code, r.json())
# Form-encoded body instead:  requests.post(url, data={"username": "a", "password": "b"})

# ============================================================
# 13. WORKING WITH APIs
# ============================================================
heading("13. WORKING WITH APIs")

# --- Query parameters: pass a dict, requests builds and URL-encodes the string ---
r = requests.get(f"{BASE}/search", params={"q": "sql injection", "limit": 5}, timeout=5)
print("final URL:", r.url)                            # spaces become %20 / +
print(r.json())

# --- Authentication headers ---
r = requests.get(f"{BASE}/items", timeout=5)                                   # no token
print("without token:", r.status_code)                                         # 401

headers = {"Authorization": "Bearer secret-token"}     # most modern APIs use Bearer tokens
r = requests.get(f"{BASE}/items", headers=headers, timeout=5)
print("with token   :", r.status_code, r.json())
# Other styles: API key header  {"X-API-Key": key}   |   Basic auth  auth=("user", "pass")
# NEVER hardcode real keys: read them from environment variables (see phase 10).

# --- Session: reuse headers + the TCP connection across many calls (faster) ---
session = requests.Session()
session.headers.update(headers)                        # sent with every request
print("session call :", session.get(f"{BASE}/items", timeout=5).status_code)

# --- Pagination: keep asking for the next page until there isn't one ---
def fetch_all(session, url, per_page=3):
    results, page = [], 1
    while page:                                        # None -> stop
        r = session.get(url, params={"page": page, "per_page": per_page}, timeout=5)
        r.raise_for_status()
        payload = r.json()
        results.extend(payload["items"])
        print(f"  page {page}: {payload['items']}")
        page = payload["next_page"]
    return results

print("all items:", fetch_all(session, f"{BASE}/items"))
# Real APIs paginate in different ways:
#   page numbers (above) | offset/limit | cursor tokens | a `Link` header
#   (GitHub: requests exposes it as r.links["next"]["url"])

# --- Retry with backoff for temporary failures (5xx, 429 rate limit) ---
import time

def get_with_retry(url, retries=4, backoff=0.2, **kwargs):
    for attempt in range(1, retries + 1):
        r = requests.get(url, timeout=5, **kwargs)
        if r.status_code not in (429, 500, 502, 503, 504):
            return r                                   # success or a non-retryable error
        # Honour the server's Retry-After header when it sends one
        wait = float(r.headers.get("Retry-After", backoff * 2 ** (attempt - 1)))
        print(f"  attempt {attempt}: got {r.status_code}, waiting {wait:.1f}s")
        time.sleep(max(wait, 0.1))
    r.raise_for_status()                               # out of retries -> raise
    return r

print(get_with_retry(f"{BASE}/flaky").json())

server.shutdown()