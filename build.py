import html, re, random, subprocess, os, sys

random.seed(241)
HERE = os.path.dirname(os.path.abspath(__file__))

def fmt(s):
    s = html.escape(s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)

# ---------- ข้อสอบ: (คำถาม, [ตัวเลือกถูกอยู่ตัวแรก, ผิด, ผิด, ผิด], คำอธิบาย) ----------
P1 = [
 ("Node.js คืออะไร?", ["JavaScript runtime ที่สร้างบน V8 engine ของ Chrome", "ภาษาโปรแกรมใหม่ที่ไม่ใช่ JavaScript", "ไลบรารีสำหรับตกแต่งหน้าเว็บ (CSS)", "ฐานข้อมูลชนิดหนึ่ง"], "Node.js = สภาพแวดล้อมรัน JS นอกเบราว์เซอร์ ใช้ V8 engine"),
 ("ข้อใด 'ไม่มี' ใน Node.js เมื่อเทียบกับ JavaScript ในเบราว์เซอร์?", ["`window` และ `document` (DOM)", "`console.log()`", "`require()`", "`process`"], "Node ไม่มี DOM จึงไม่มี window/document และไม่มี cookies แบบเบราว์เซอร์"),
 ("สถาปัตยกรรมของ Node.js คือแบบใด?", ["Single thread event loop แบบ non-blocking", "Multi-thread ทุก request มี thread ของตัวเอง", "รอให้ request หนึ่งเสร็จก่อนจึงรับ request ถัดไป", "ใช้ process แยกต่อ 1 ผู้ใช้"], "Thread หลักรับ request แล้วส่งงานให้หน่วยอื่น ไม่รอ จึงรับ request ถัดไปได้ทันที"),
 ("งานแบบใดที่ Node.js 'ไม่' เหมาะ?", ["งานที่ใช้การคำนวณหนัก (computation-intensive)", "งานที่เน้น I/O มาก", "แอปแบบ real-time", "JSON API"], "Node เหมาะกับ I/O และ real-time แต่ไม่เหมาะกับงานคำนวณหนัก"),
 ("คำสั่งใดใช้รันไฟล์ `app.js` ใน Node.js?", ["`node app.js`", "`run app.js`", "`js app.js`", "`npm app.js`"], "รันด้วย `node ชื่อไฟล์.js` ผ่าน command line"),
 ("`module.exports` ใช้ทำอะไร?", ["เปิดเผย (export) ฟังก์ชัน/ค่า ให้ไฟล์อื่นนำไปใช้", "นำเข้า module จากไฟล์อื่น", "ลบ module ออกจากโปรเจกต์", "สร้างเซิร์ฟเวอร์"], "`module.exports` = ส่งออก, `require()` = นำเข้า"),
 ("ถ้าต้องการโหลดไฟล์ module ของเราเองชื่อ `hello.js` ในโฟลเดอร์เดียวกัน ควรเขียนอย่างไร?", ["`require('./hello')`", "`require('hello')`", "`import hello.js`", "`include('hello')`"], "ไฟล์ของเราเองต้องใช้ relative path เช่น `./hello`"),
 ("ใน path module ผลของ `path.parse()` ที่ field `base` คืออะไร?", ["ชื่อไฟล์พร้อมนามสกุล เช่น `path.js`", "เฉพาะนามสกุล เช่น `.js`", "เฉพาะชื่อไฟล์ เช่น `path`", "โฟลเดอร์ราก `/`"], "root=ราก, dir=โฟลเดอร์, base=ชื่อ+นามสกุล, name=ชื่อ, ext=นามสกุล"),
 ("ข้อใดเป็นข้อแตกต่างของ `fs.readFileSync` กับ `fs.readFile`?", ["`readFileSync` เป็น blocking ต้องรออ่านเสร็จก่อนทำบรรทัดถัดไป", "`readFileSync` เร็วกว่าเสมอและไม่ block", "`readFile` ต้องรอจนเสร็จก่อนบรรทัดถัดไป", "ทั้งสองเหมือนกันทุกประการ"], "Sync = blocking (ลำดับแน่นอน), Async = non-blocking (ใช้ callback ลำดับเสร็จอาจสลับ)"),
 ("ใน `http.createServer((req, res) => {...})` บรรทัดใดใช้ 'จบ' การตอบกลับ?", ["`res.end()`", "`res.write()`", "`res.setHeader()`", "`myServer.listen()`"], "`res.end()` ปิดการตอบกลับ ส่วน `listen()` ใช้เปิดพอร์ตรอรับ request"),
]

P2 = [
 ("Express คืออะไร?", ["web framework ขนาดเล็กและยืดหยุ่นสำหรับ Node.js", "ฐานข้อมูล", "ตัวแก้ไขโค้ด", "ภาษาสำหรับทำ template"], "Express ช่วยเรื่อง routing, API และทำงานร่วมกับ template engine (Pug, EJS)"),
 ("คำสั่ง `npm init` สร้างไฟล์ใด?", ["`package.json`", "`app.js`", "`.env`", "`node_modules`"], "`package.json` เก็บ metadata ของโปรเจกต์ เช่น ชื่อ เวอร์ชัน entry point"),
 ("หลังรัน `npm install express` ชื่อ express จะไปอยู่ส่วนใดของ package.json?", ["`dependencies`", "`scripts`", "`author`", "`main`"], "แพ็กเกจที่ติดตั้งจะถูกบันทึกใน `dependencies`"),
 ("`nodemon` มีประโยชน์อย่างไร?", ["รีสตาร์ทโปรแกรมให้อัตโนมัติเมื่อไฟล์เปลี่ยน", "เข้ารหัสรหัสผ่าน", "เชื่อมต่อฐานข้อมูล", "แปลง JS เป็น HTML"], "nodemon เฝ้าดูไฟล์และ restart server ให้เอง ใช้ตอนพัฒนา"),
 ("โค้ดใดสร้าง route ที่ตอบ GET ที่ path `/` ด้วยข้อความ?", ["`app.get('/', (req, res) => res.send('Hi'))`", "`app.post('/', ...)`", "`app.listen('/', ...)`", "`app.use.get('Hi')`"], "รูปแบบ: `app.get(path, (req, res) => {...})` และ `res.send()` ส่งข้อความกลับ"),
 ("`app.use('/product', router1)` และใน router1 มี `router1.get('/add', ...)` URL ที่เข้าถึงได้คือ?", ["`/product/add`", "`/add`", "`/product`", "`/router1/add`"], "path ที่ mount (`/product`) ต่อกับ path ใน router (`/add`)"),
 ("ในการส่งไฟล์ HTML กลับ ใช้เมธอดใดของ `res`?", ["`res.sendFile()`", "`res.cookie()`", "`res.query()`", "`res.parse()`"], "ใช้ `res.sendFile(path.join(__dirname, 'html/x.html'))`"),
 ("`router.use((req,res)=>{ res.status(404).send(...) })` ควรวางไว้ตรงไหน เพื่อจับ path ที่ไม่มีใครรองรับ?", ["ท้ายสุด หลัง route อื่นทั้งหมด", "บนสุด ก่อน route อื่น", "ในไฟล์ HTML", "ใน package.json"], "Express ไล่ตามลำดับ ถ้าวาง 404 ไว้บนสุดจะดักทุกเส้นทางก่อน"),
 ("ต้องใช้ middleware ใดเพื่อให้ไฟล์ CSS/รูปภาพ (static files) ทำงาน?", ["`express.static`", "`express.json`", "`express.Router`", "`express.urlencoded`"], "`app.use('/', express.static(path.join(__dirname,'public')))`"),
 ("ฟอร์มส่งแบบ POST จะอ่านค่าได้จากที่ใด (และต้องมี `express.urlencoded`)?", ["`req.body`", "`req.query`", "`req.cookies`", "`req.url`"], "GET → `req.query`, POST → `req.body` (ต้องมี middleware ช่วย parse)"),
]

P3 = [
 ("คำสั่ง `npm install` (ไม่ระบุชื่อแพ็กเกจ) ใช้เมื่อใด?", ["ติดตั้ง dependencies ทั้งหมดตาม package.json หลัง clone โปรเจกต์", "สร้างโปรเจกต์ใหม่", "ลบแพ็กเกจทั้งหมด", "รันเซิร์ฟเวอร์"], "`npm install` อ่าน package.json แล้วติดตั้งทุก dependency"),
 ("ไฟล์ `.env` และแพ็กเกจ `dotenv` มีไว้ทำอะไร?", ["เก็บค่าตั้งค่า (เช่น PORT) แล้วโหลดเข้า `process.env`", "เก็บโค้ด HTML", "ทำให้เว็บเร็วขึ้น", "จัดรูปแบบ CSS"], "แยกค่าตั้งค่าออกจากโค้ด ไม่ hardcode และโค้ดเดียวกันรันได้หลายเครื่อง"),
 ("คำว่า HTTP เป็น 'stateless' หมายถึงอะไร?", ["แต่ละ request ไม่มีความเชื่อมโยงกัน", "เซิร์ฟเวอร์จำผู้ใช้ทุกคนได้เสมอ", "ข้อมูลถูกเข้ารหัสเสมอ", "ใช้ได้เฉพาะ GET"], "จึงต้องใช้ cookie/session เพื่อให้จำได้ว่า request มาจากเบราว์เซอร์เดียวกัน"),
 ("Cookie และ Session เก็บข้อมูลที่ใด?", ["Cookie ที่ฝั่ง client, Session ที่ฝั่ง server", "Cookie ที่ server, Session ที่ client", "ทั้งคู่ที่ client", "ทั้งคู่ที่ฐานข้อมูล"], "Cookie อยู่ที่เบราว์เซอร์ (ผู้ใช้อ่านได้) ส่วน Session อยู่ฝั่ง server (ป้องกันจากผู้ใช้)"),
 ("ต้องติดตั้งแพ็กเกจใดเพื่ออ่าน `req.cookies`?", ["`cookie-parser`", "`express-session`", "`mysql2`", "`nodemon`"], "ใช้ `router.use(cp())` หลัง `require('cookie-parser')`"),
 ("คำสั่งใดสร้างและลบ cookie ตามลำดับ?", ["`res.cookie()` และ `res.clearCookie()`", "`req.cookie()` และ `req.delete()`", "`res.setSession()` และ `res.endSession()`", "`cookie.add()` และ `cookie.remove()`"], "สร้าง `res.cookie(name,value)`, ลบ `res.clearCookie(name)`"),
 ("`res.cookie('a','b',{maxAge: 360000})` ค่า 360000 มีหน่วยเป็น?", ["มิลลิวินาที", "วินาที", "นาที", "ชั่วโมง"], "maxAge หน่วยเป็น millisecond (360000 ms = 6 นาที)"),
 ("ข้อใดถูกต้องเกี่ยวกับ `express-session` และ MemoryStore?", ["MemoryStore ไม่ออกแบบมาให้ใช้จริงบน production", "MemoryStore เหมาะที่สุดสำหรับ production", "ต้องมี MemoryStore ทุกครั้ง", "express-session เก็บข้อมูลที่ client"], "MemoryStore ใช้ตอน debug/พัฒนา ส่วน production ควรใช้ session store อื่น"),
 ("แพ็กเกจใดใช้เชื่อมต่อ MySQL ในรายวิชานี้ และคำสั่งใดรัน SQL?", ["`mysql2` และ `connection.query()`", "`mysql2` และ `res.query()`", "`express-sql` และ `app.sql()`", "`dotenv` และ `connection.run()`"], "ใช้ `mysql.createConnection({...})` แล้ว `connection.query(sql, callback)`"),
 ("หลัง `INSERT` สำเร็จ จำนวนแถวที่ถูกเพิ่มดูได้จากอะไร?", ["`results.affectedRows`", "`results.length`", "`req.query`", "`res.rows`"], "INSERT/UPDATE/DELETE ดู `affectedRows`; SELECT ได้ array ของแถว ดู `results.length`"),
]

FINAL = [
 # จาก Part 1
 ("ข้อใดเป็น global object ที่ใช้ได้ทุกไฟล์โดยไม่ต้อง import?", ["`__dirname`", "`window`", "`document`", "`localStorage`"], "Global ของ Node เช่น `__dirname`, `__filename`, `module`, `require`, `process`, `global`"),
 ("ไฟล์ A และ B ต่างมีฟังก์ชัน `sayHello()` ของตัวเอง จะเกิดอะไรขึ้น?", ["ไม่ทับกัน เพราะแต่ละไฟล์เป็น module ที่มี scope ของตัวเอง", "ฟังก์ชันของไฟล์หลังทับไฟล์แรก", "เกิด error ทันที", "ต้องเปลี่ยนชื่อก่อน"], "ทุกไฟล์ใน Node เป็น module ตัวแปร/ฟังก์ชัน private ภายในไฟล์"),
 ("`new URL('https://x.com:8080/a/b?time=now').searchParams.get('time')` ได้ค่าใด?", ["`now`", "`8080`", "`/a/b`", "`https:`"], "searchParams อ่านค่า query string หลัง `?`"),
 ("`path.join(__dirname, 'test.js')` มีไว้ทำอะไร?", ["ต่อ path เป็นเส้นทางเดียวโดยจัดการให้เหมาะกับ OS", "อ่านเนื้อหาไฟล์", "ลบไฟล์", "เริ่มเซิร์ฟเวอร์"], "path module จัดการเรื่อง `/` กับ `\\` ต่างกันของแต่ละ OS ให้อัตโนมัติ"),
 ("การซ้อน callback ของ `fs.readFile` หลายชั้นจนอ่านยาก เรียกว่าอะไร และมีทางแก้ใด?", ["Callback hell แก้ด้วย Promise หรือ async/await", "Event loop แก้ด้วย nodemon", "Middleware แก้ด้วย Router", "Stateless แก้ด้วย cookie"], "Callback hell = `})` ซ้อนเป็นขั้นบันได โค้ดอ่านและดูแลยาก"),
 ("อ่านไฟล์ 3 ไฟล์ด้วย `fs.readFile` (async) แล้วรันหลายครั้ง ผลลัพธ์จะเป็นอย่างไร?", ["ลำดับการแสดงผลอาจไม่เหมือนกันทุกครั้ง", "เรียงตามลำดับโค้ดเสมอ", "แสดงเพียงไฟล์แรก", "เกิด error ทุกครั้ง"], "async ไม่รอกัน ไฟล์ไหนอ่านเสร็จก่อนก็แสดงก่อน"),
 ("ข้อใดจริงเกี่ยวกับ server-side code?", ["เข้าถึง file system และ OS ของเซิร์ฟเวอร์ได้เต็มที่", "รันในเบราว์เซอร์ของผู้ใช้", "เขียนได้เฉพาะ HTML/CSS", "ผู้ใช้เปิดดูซอร์สโค้ดได้ทั้งหมด"], "Client-side = HTML/CSS/JS รันในเบราว์เซอร์; Server-side เลือกว่าจะส่งเนื้อหาอะไรกลับ"),
 ("ใน server ที่ `listen(8081)` ผู้ใช้เปิดเบราว์เซอร์ที่ใด จึงเข้าถึงได้?", ["`http://localhost:8081`", "`http://localhost`", "`http://8081:localhost`", "`https://localhost:3000`"], "รูปแบบ host:port → `localhost:8081`"),
 ("ถ้า request เป็น 'static resource' เว็บเซิร์ฟเวอร์จะทำอย่างไร?", ["ส่งไฟล์กลับไปทันที ไม่ต้องผ่าน web application", "ส่งไปถามฐานข้อมูลก่อนเสมอ", "ปฏิเสธ request", "สร้างหน้า HTML ใหม่ทุกครั้ง"], "เฉพาะ dynamic resource เท่านั้นที่ส่งต่อให้ server-side code"),
 ("จะหยุดเซิร์ฟเวอร์ที่รันอยู่ใน terminal ใช้ปุ่มใด?", ["Ctrl + C", "Ctrl + V", "Ctrl + S", "Esc"], "กด Ctrl+C เพื่อหยุดโปรแกรมที่รันอยู่"),
 # จาก Part 2
 ("Template engine ที่สไลด์กล่าวถึงคือข้อใด?", ["Pug และ EJS", "MySQL และ Oracle", "Bootstrap และ Tailwind", "Git และ GitHub"], "template engine แทนที่ตัวแปรในไฟล์ template ด้วยค่าจริง แล้วสร้างเป็น HTML"),
 ("`\"start\": \"nodemon app.js\"` ใน scripts ทำให้รันโปรเจกต์ด้วยคำสั่งใด?", ["`npm start`", "`npm run app`", "`node start`", "`nodemon start.js`"], "ตั้ง script `start` แล้วรันด้วย `npm start`"),
 ("Middleware คืออะไร?", ["ฟังก์ชันที่เข้าถึง request (req) และ response (res) ได้", "ตัวเชื่อมฐานข้อมูล", "ไฟล์ HTML ชนิดหนึ่ง", "คำสั่ง npm"], "ตัวอย่าง: `express.static`, `express.json`, `cookie-parser`, `session`"),
 ("ฟอร์ม `<form action=\"/form-get\" method=\"GET\">` ส่งมา เซิร์ฟเวอร์ต้องมี route ใด?", ["`router.get('/form-get', ...)`", "`router.post('/form-get', ...)`", "`router.get('/form-post', ...)`", "`router.use('/form', ...)`"], "path ต้องตรงกับ `action` และ method ต้องตรงกับ `method`"),
 ("URL `/form-get?fname=John&lname=Doe` ค่า `req.query.fname` คือ?", ["`John`", "`Doe`", "`fname`", "`undefined`"], "`req.query` เก็บพารามิเตอร์หลัง `?` เป็น object"),
 ("`express.json()` ทำหน้าที่อะไร?", ["parse request body ที่เป็น JSON", "ส่ง JSON กลับไปที่ client", "สร้างไฟล์ JSON", "อ่านค่า `.env`"], "ส่วน `express.urlencoded()` parse ข้อมูลจากฟอร์ม"),
 ("ถ้า HTML เรียก `href=\"../public/mystyle.css\"` แล้ว CSS ไม่ทำงาน เพราะอะไร?", ["ยังไม่ได้ตั้งโฟลเดอร์ static ด้วย `express.static`", "ไฟล์ CSS ผิดภาษา", "ต้องใช้ POST", "ต้องติดตั้ง mysql2"], "หลังตั้ง static ที่ `public` ให้อ้างเป็น `/mystyle.css`"),
 ("`package.json` ฟิลด์ `main` ระบุอะไร?", ["entry point (ไฟล์เริ่มต้น) ของโปรเจกต์", "ชื่อผู้เขียน", "รหัสผ่านฐานข้อมูล", "พอร์ตของเซิร์ฟเวอร์"], "เช่น `\"main\": \"app.js\"`"),
 ("`res.status(401).end(...)` ใช้สื่อความหมายใด?", ["ไม่ได้รับอนุญาต (ต้องมี cookie/สิทธิ์ก่อน)", "สำเร็จ", "ไม่พบหน้า", "เซิร์ฟเวอร์ล่ม"], "200=OK, 404=Not Found, 401=Unauthorized"),
 ("ถ้าเข้า URL ที่ไม่มี route ใดรองรับ และมี 404 handler อยู่ท้ายสุด ผู้ใช้จะเห็นอะไร?", ["ข้อความ 'Invalid Path' พร้อมสถานะ 404", "หน้าแรก", "ข้อความ Hello World", "เซิร์ฟเวอร์ปิดตัวเอง"], "`router.use` ท้ายสุดดักทุกเส้นทางที่ไม่ตรง"),
 # จาก Part 3
 ("ต้องเรียกอะไรก่อนอ่าน `process.env.PORT` ได้?", ["`dotenv.config()`", "`cookie-parser`", "`connection.connect()`", "`express.static`"], "`dotenv.config()` โหลดตัวแปรจาก `.env` เข้า `process.env`"),
 ("เหตุผลที่ควรใช้ environment variable คืออะไร?", ["ไม่ต้อง hardcode ค่า และย้ายโค้ดไปรันที่อื่นได้", "ทำให้โค้ดสั้นลงเท่านั้น", "ใช้แทนฐานข้อมูล", "ทำให้เบราว์เซอร์เร็วขึ้น"], "ค่า เช่น PORT, DB_USER อยู่นอกซอร์สโค้ด"),
 ("ทำไมไม่ควรเก็บข้อมูลลับ (เช่น รหัสผ่าน) ใน cookie?", ["เพราะอยู่ฝั่ง client และผู้ใช้อ่านได้", "เพราะ cookie ใหญ่เกินไป", "เพราะ cookie ใช้ไม่ได้ใน Node", "เพราะ cookie ลบไม่ได้"], "ข้อมูลที่ต้องปกป้องควรเก็บใน session ฝั่ง server"),
 ("ในตัวอย่าง `/restrict` ถ้าไม่มี cookie `tokenID` จะเกิดอะไร?", ["ตอบ 401 พร้อมข้อความ error", "แสดงเนื้อหาลับ", "ตอบ 404", "สร้าง cookie ให้อัตโนมัติ"], "โค้ดตรวจ `req.cookies['tokenID']` ถ้าไม่มีให้ส่ง 401"),
 ("ใน `express-session` ตัวเลือก `secret` มีไว้ทำอะไร?", ["ลงนาม (sign) session ID", "เก็บรหัสผ่านฐานข้อมูล", "กำหนดพอร์ต", "ตั้งอายุ cookie"], "ค่า secret ควรเก็บใน `.env` เช่น `SESSION_SECRET`"),
 ("เข้า `/pageview` ครั้งแรกตั้ง `numviews = 1` และครั้งถัดไปบวกเพิ่ม เข้าครั้งที่ 3 ค่า `numviews` คือ?", ["3", "1", "2", "0"], "ครั้งแรก=1, ครั้งที่สอง=2, ครั้งที่สาม=3 (ค่าอยู่ใน session)"),
 ("SQL ใดดึงชื่อและรหัสวิชาของภาควิชา CIS?", ["`SELECT course_code, course_name FROM Course WHERE dept_code='CIS'`", "`INSERT INTO Course WHERE dept_code='CIS'`", "`DELETE course_code FROM Course`", "`UPDATE Course SELECT dept_code`"], "SELECT ... FROM ... WHERE เงื่อนไข"),
 ("`connection.connect(function(err){ if(err) throw err; ... })` ส่วน `err` หมายถึง?", ["ข้อผิดพลาดตอนเชื่อมต่อฐานข้อมูล (ถ้ามี)", "ชื่อฐานข้อมูล", "จำนวนแถวผลลัพธ์", "รหัสผ่าน"], "ถ้าเชื่อมต่อไม่สำเร็จ `err` จะมีค่าและโปรแกรม throw error"),
 ("ในทางปฏิบัติ การเพิ่มข้อมูลใหม่ (INSERT) ผ่านเว็บควรใช้ HTTP method ใด?", ["POST", "GET", "HEAD", "ไม่ต้องใช้ method"], "สไลด์ใช้ GET เพื่อสาธิตเท่านั้น ปกติใช้ POST"),
 ("ใน express-session ตัวเลือก `saveUninitialized: true` หมายถึงอะไร?", ["สร้าง session ให้ผู้ใช้ทุกคน แม้ยังไม่ได้เก็บข้อมูลอะไร", "บันทึก session เฉพาะเมื่อมีการเปลี่ยนแปลง", "ลบ session ทุกครั้งที่ปิดเบราว์เซอร์", "เก็บ session ไว้ที่ฝั่ง client"], "`resave: false` = บันทึกเมื่อ session เปลี่ยน · `saveUninitialized: true` = สร้างให้ทุกคนแม้ยังไม่ใช้"),
]

# ---------- สรุปเนื้อหา ----------
S1 = """
<div class="grid2">
 <div class="card"><h4>1) Client vs Server</h4>
  <ul><li><b>Client-side</b> = HTML, CSS, JS รันในเบราว์เซอร์</li>
  <li><b>Server-side</b> = เลือกว่าจะส่งเนื้อหาอะไรกลับ (PHP, Python, Ruby, C#, <b>Node.js</b>) เข้าถึง file system ของเครื่องได้เต็มที่</li></ul></div>
 <div class="card"><h4>2) ลำดับ Request / Response</h4>
  <ol><li>Client ส่ง HTTP GET ไปที่ Web Server</li><li>เป็น static → ส่งไฟล์กลับเลย</li><li>เป็น dynamic → ส่งต่อให้ Web Application อ่าน DB</li><li>นำข้อมูลรวมกับ HTML template แล้วตอบกลับ</li></ol></div>
</div>
<div class="note"><b>Server = IP + Port</b> เช่น <code>localhost:3000</code>, <code>10.34.111.111:8080</code> พอร์ตที่เจอบ่อย: 3000, 8080, 8081</div>

<h3>Node.js คืออะไร</h3>
<ul>
<li><b>Asynchronous JavaScript runtime</b> สร้างบน <b>V8 engine</b> ของ Chrome — open-source server environment</li>
<li><b>ไม่มี</b> DOM (<code>document</code>, <code>window</code>) และไม่มี Cookies แบบเบราว์เซอร์ แต่มี module พิเศษ เช่น File system, HTTP</li>
<li><b>Single thread event loop</b>: thread หลักรับ request → ส่งงานให้ File System / Database / Computation → <b>ไม่รอ (non-blocking)</b> รับ request ถัดไปได้ทันที → งานเสร็จค่อยตอบกลับ</li>
</ul>
<div class="grid2">
 <div class="good"><b>เหมาะกับ</b><br>I/O หนัก, real-time, scalable, JSON API, ใช้ JS ภาษาเดียวทั้งระบบ</div>
 <div class="bad"><b>ไม่เหมาะกับ</b><br>งานคำนวณหนัก (computation-intensive)</div>
</div>

<h3>เริ่มใช้งาน + Global Objects</h3>
<ul><li>ติดตั้ง LTS จาก nodejs.org · ตรวจด้วย <code>node --version</code> · รันด้วย <code>node filename.js</code></li>
<li><code>console.log()</code> ใน Node ไม่ใช่ <code>window.console.log()</code></li>
<li><b>Global objects</b> ใช้ได้ทุกไฟล์ ไม่ต้อง import: <code>__dirname</code> (โฟลเดอร์ปัจจุบัน), <code>__filename</code> (path เต็มของไฟล์), <code>exports</code>, <code>module</code>, <code>require()</code>, <code>console</code>, <code>process</code>, <code>global</code></li></ul>

<h3>Module System</h3>
<ul><li><b>ทุกไฟล์ JS = 1 module</b> ตัวแปร/ฟังก์ชันเป็น private ภายในไฟล์ ชื่อซ้ำกันข้ามไฟล์ไม่ทับกัน</li></ul>
<pre><span class="c">// hello.js — ส่งออก (export)</span>
function sayHello(){ console.log("Hello"); }
module.exports.sayHi = sayHello;

<span class="c">// app.js — นำเข้า (import)</span>
const eng = require("./hello");   <span class="c">// ไฟล์ของเรา ใช้ ./ นำหน้า</span>
eng.sayHi();                       <span class="c">// → Hello</span></pre>
<p class="tip">export ได้ทั้งค่าตรง ๆ <code>module.exports = "Hello"</code>, property <code>module.exports.x = ...</code>, หรือฟังก์ชัน</p>

<h3>Built-in Modules ที่ต้องรู้</h3>
<table>
<tr><th>Module</th><th>หน้าที่</th><th>ของสำคัญ</th></tr>
<tr><td><code>path</code></td><td>จัดการ path ให้เหมาะกับแต่ละ OS</td><td><code>resolve()</code>, <code>join()</code>, <code>extname()</code>, <code>parse()</code> → <code>root, dir, base, name, ext</code></td></tr>
<tr><td><code>url</code></td><td>แยกส่วนประกอบ URL</td><td><code>new URL(str)</code> → <code>href, protocol, host, port, pathname, search, searchParams.get('key')</code></td></tr>
<tr><td><code>fs</code></td><td>จัดการไฟล์</td><td><code>readFile</code>, <code>writeFile</code>, <code>appendFile</code>, <code>unlink</code> (ลบ), <code>rename</code> — ทุกตัวมีคู่ <b>Sync</b></td></tr>
<tr><td><code>http</code></td><td>สร้าง web server</td><td><code>createServer()</code>, <code>listen(port)</code></td></tr>
</table>

<h3>fs: Async vs Sync และ Callback Hell</h3>
<div class="grid2">
 <div class="card"><h4>Async (non-blocking)</h4><p>ใช้ callback <code>function(err, contents)</code> อ่าน 3 ไฟล์พร้อมกัน → <b>ลำดับผลลัพธ์อาจสลับกันได้</b> ในแต่ละครั้งที่รัน</p></div>
 <div class="card"><h4>Sync (blocking)</h4><p><code>readFileSync</code> รอจนเสร็จก่อนบรรทัดถัดไป → <b>ลำดับแน่นอน</b> แต่หยุดการทำงานอื่น</p></div>
</div>
<ul><li>อยากการันตีลำดับ: ใช้ Sync หรือซ้อน callback</li>
<li>ซ้อน callback เป็นขั้นบันได <code>})</code> = <b>Callback Hell</b> (อ่านยาก ดูแลยาก) → ใช้ <b>Promise</b> หรือ <b>async/await</b> แทน</li></ul>

<h3>สร้าง Server ด้วย http</h3>
<pre>const http = require("http");
const myServer = http.createServer((req, res) => {
  res.statusCode = 200;                          <span class="c">// 200 = OK</span>
  res.setHeader("Content-Type", "text/plain");
  res.write("Hello World!");
  res.end();                                     <span class="c">// จบการตอบกลับ</span>
});
myServer.listen(8081, () => console.log("Listening on 8081"));</pre>
<ul><li><code>req.url</code> = path ที่ขอ, <code>req.method</code> = GET/POST · เปิด <code>http://localhost:8081</code> · หยุดด้วย <b>Ctrl+C</b></li>
<li>เบราว์เซอร์มักขอ <code>/favicon.ico</code> เพิ่มอีก 1 request</li></ul>
<h4>Routing เอง (if / else if)</h4>
<pre>if (req.url === "/")           { /* ข้อความ greeting */ }
else if (req.url === "/shabu") { fs.readFile("./shabu.html", ...) <span class="c">// Content-Type: text/html</span> }
else if (req.url === "/bbq")   { /* ส่ง bbq.html */ }
else { res.statusCode = 404; res.write("Invalid requested :("); res.end(); }</pre>
"""

S2 = """
<h3>Express Framework</h3>
<ul><li>web framework ที่ <b>minimal และ flexible</b> ช่วยเรื่อง <b>routing</b>, สร้าง <b>API</b>, ใช้ร่วมกับ <b>template engine</b> (Pug, EJS) ที่แทนตัวแปรในไฟล์ template ด้วยค่าจริงแล้วสร้างเป็น HTML</li></ul>

<h3>ตั้งโปรเจกต์ Express (ทำตามลำดับ)</h3>
<table>
<tr><th>ขั้น</th><th>คำสั่ง / ทำอะไร</th><th>ผล</th></tr>
<tr><td>1</td><td><code>npm init</code></td><td>สร้าง <code>package.json</code> (metadata, entry point <code>main</code>)</td></tr>
<tr><td>2</td><td><code>npm install express</code></td><td>ลง Express + เพิ่มใน <code>dependencies</code></td></tr>
<tr><td>3</td><td><code>npm install nodemon</code></td><td>restart server อัตโนมัติเมื่อไฟล์เปลี่ยน (ไม่บังคับ)</td></tr>
<tr><td>4</td><td>สร้าง <code>app.js</code></td><td>ไฟล์หลัก: routes + ตั้งค่า server</td></tr>
<tr><td>5</td><td>ใน scripts ใส่ <code>"start": "nodemon app.js"</code></td><td>รันด้วย <code>npm start</code></td></tr>
</table>
<p class="tip">npm = package manager สำหรับติดตั้งแพ็กเกจเพิ่มให้ Node.js · โครงโฟลเดอร์: <code>node_modules/</code>, <code>package.json</code>, <code>app.js</code>, <code>html/</code></p>

<h3>โครง app.js พื้นฐาน</h3>
<pre>const express = require('express');
const port = 3000;
const app = express();                       <span class="c">// สร้างแอป</span>

app.get('/', (req, res) => {                  <span class="c">// route: GET /</span>
  res.send('Hello World from Root!');
});

app.listen(port, () => console.log(`Server listening on port: ${port}`));</pre>

<h3>Routing ด้วย express.Router()</h3>
<ul><li><b>Middleware</b> = ฟังก์ชันที่เข้าถึง <code>req</code> และ <code>res</code> ได้</li>
<li>เส้นทางหนึ่งประกอบด้วย <b>HTTP method + path</b> เช่น <code>GET /shabu</code>, <code>POST /user/add</code></li></ul>
<pre>const router = express.Router();
app.use(router);                              <span class="c">// ลงทะเบียน router</span>

router.get('/shabu', (req, res) => {
  res.sendFile(path.join(`${__dirname}/html/shabu.html`));  <span class="c">// ส่งไฟล์ HTML</span>
});

<span class="c">// ★ วางท้ายสุด: ดักทุก path ที่ไม่มีใครรับ (ทุก method)</span>
router.use((req, res, next) => {
  res.status(404).send("Invalid Path");
});</pre>
<div class="note"><b>จำ:</b> <code>__dirname</code> = path โฟลเดอร์ปัจจุบัน · <code>path.join</code> = ต่อ path · ลิงก์ใน navbar <code>href="/shabu"</code> ต้องตรงกับ route ใน <code>app.js</code></div>

<h3>Serving Static Files (CSS / รูป / JS ฝั่ง client)</h3>
<pre>app.use('/', express.static(path.join(__dirname, 'public')));   <span class="c">// ตั้งโฟลเดอร์ static</span>
<span class="c">&lt;!-- ใน HTML อ้างจากโฟลเดอร์ static เป็น root --&gt;</span>
&lt;link rel="stylesheet" href="/mystyle.css"&gt;   <span class="c">// ไม่ใช่ ../public/mystyle.css</span></pre>

<h3>Modular Routes (เว็บใหญ่ขึ้น)</h3>
<pre>app.use("/product", router1);      router1.get('/add', ...)  <span class="c">→ /product/add</span>
app.use("/user",    router2);      router2.get('/add', ...)  <span class="c">→ /user/add</span></pre>
<p class="tip">path ที่ mount (<code>/product</code>) + path ใน router (<code>/add</code>) = URL เต็ม</p>

<h3>Form Handling: GET vs POST</h3>
<ul><li>ตรวจข้อมูลที่เบราว์เซอร์ (HTML5/JS) เมื่อทำได้ และตรวจซ้ำที่ server ถ้าจะลง DB</li>
<li>แอตทริบิวต์ใน <code>&lt;form&gt;</code>: <b>action</b> = ปลายทาง (เช่น <code>/form-get</code>) · <b>method</b> = GET/POST · ค่าอ้างผ่านแอตทริบิวต์ <b>name</b> ของ input</li>
<li><b>path และ method ใน route ต้องตรงกับ action และ method ในฟอร์ม</b></li></ul>
<table>
<tr><th></th><th>GET</th><th>POST</th></tr>
<tr><td>ข้อมูลอยู่ที่</td><td>URL หลัง <code>?</code> เช่น <code>?fname=John&amp;lname=Doe</code></td><td>message body</td></tr>
<tr><td>อ่านใน Express</td><td><code>req.query.fname</code></td><td><code>req.body.fname</code></td></tr>
<tr><td>ต้องมี middleware?</td><td>ไม่ต้อง</td><td>ต้อง: <code>express.json()</code> และ <code>express.urlencoded({extended:true})</code></td></tr>
<tr><td>route</td><td><code>router.get("/form-get", ...)</code></td><td><code>router.post("/form-post", ...)</code></td></tr>
</table>
<pre>router.use(express.json());                        <span class="c">// parse JSON payload</span>
router.use(express.urlencoded({ extended: true })); <span class="c">// parse ข้อมูลจากฟอร์ม</span>
router.post("/form-post", (req, res) => {
  res.send(`Form submitted by ${req.body.fname} ${req.body.lname} with ${req.method}`);
});</pre>
"""

S3 = """
<h3>สรุป npm ที่ต้องรู้</h3>
<table>
<tr><th>คำสั่ง</th><th>ใช้เมื่อ</th></tr>
<tr><td><code>npm init</code></td><td>สร้างโปรเจกต์ (ถามทีละข้อ)</td></tr>
<tr><td><code>npm init -y</code></td><td>สร้างโปรเจกต์ด้วยค่า default (ข้ามคำถาม)</td></tr>
<tr><td><code>npm install</code></td><td>ติดตั้ง dependencies ทั้งหมดใน package.json (หลัง clone/pull)</td></tr>
<tr><td><code>npm install &lt;package&gt;</code></td><td>เพิ่มไลบรารีใหม่ เช่น express</td></tr>
<tr><td><code>npm uninstall &lt;package&gt;</code></td><td>เอาแพ็กเกจที่ไม่ใช้แล้วออก</td></tr>
</table>

<h3>Environment Variable (.env)</h3>
<ul><li>คู่ <b>key=value</b> เก็บค่าตั้งค่า (PORT, API_KEY, DB_HOST, DB_NAME) <b>อยู่นอกซอร์สโค้ด</b> → ไม่ต้อง hardcode, รันได้หลายเครื่อง/cloud, ดูแลง่าย</li></ul>
<div class="grid2">
<pre># .env
PORT=3000
SESSION_SECRET=mysecretkey</pre>
<pre>const dotenv = require("dotenv");
dotenv.config();            <span class="c">// โหลด .env</span>
app.listen(process.env.PORT, ...)</pre>
</div>
<p class="tip">ติดตั้ง <code>npm install dotenv</code> → สร้าง <code>.env</code> ที่ root → <code>dotenv.config()</code> → อ่านด้วย <code>process.env.ชื่อ</code></p>

<h3>HTTP Stateless → Cookie และ Session</h3>
<ul><li>HTTP เป็น <b>stateless</b>: แต่ละ request ไม่เกี่ยวข้องกัน → ใช้ <b>cookie</b> ช่วยให้เซิร์ฟเวอร์รู้ว่า request มาจากเบราว์เซอร์เดียวกัน (session management, personalization, tracking)</li></ul>
<table>
<tr><th></th><th>Cookie</th><th>Session</th></tr>
<tr><td>เก็บที่</td><td><b>Client</b> (เบราว์เซอร์)</td><td><b>Server</b></td></tr>
<tr><td>ผู้ใช้อ่านได้?</td><td>อ่านได้ → ไม่ควรเก็บความลับ</td><td>ป้องกันจากผู้ใช้</td></tr>
<tr><td>แพ็กเกจ</td><td><code>cookie-parser</code></td><td><code>express-session</code></td></tr>
</table>

<h3>Cookie ใน Express</h3>
<ul><li>เซิร์ฟเวอร์ส่งเฮดเดอร์ <code>Set-Cookie</code> → เบราว์เซอร์เก็บ → ส่งกลับในเฮดเดอร์ <code>Cookie</code> ทุก request</li></ul>
<pre>const cp = require("cookie-parser");
router.use(cp());                                   <span class="c">// ต้องมีก่อนอ่าน req.cookies</span>

res.cookie('tokenID', 'some-random-id');            <span class="c">// สร้าง</span>
req.cookies;                                        <span class="c">// อ่านทั้งหมด</span>
req.cookies['tokenID'];                             <span class="c">// อ่านตามชื่อ</span>
res.cookie('x', 'v', { maxAge: 360000 });           <span class="c">// อายุ (มิลลิวินาที)</span>
res.clearCookie('tokenID');                         <span class="c">// ลบ</span></pre>
<div class="note"><b>ตัวอย่าง Login/Logout:</b> <code>/login</code> สร้างคุกกี้ <code>tokenID</code> · <code>/restrict</code> ตรวจคุกกี้ ถ้าไม่มีตอบ <b>401</b> · <code>/logout</code> ใช้ <code>clearCookie</code> (จริง ๆ ต้องตรวจ user/password ก่อนสร้าง token)</div>

<h3>Session ใน Express</h3>
<pre>const session = require('express-session');
router.use(session({
  secret: process.env.SESSION_SECRET,  <span class="c">// ลงนาม session ID</span>
  resave: false,                       <span class="c">// บันทึกเฉพาะเมื่อ session เปลี่ยน</span>
  saveUninitialized: true,             <span class="c">// สร้าง session ให้ทุกผู้ใช้ แม้ยังไม่ใช้</span>
}));

req.session.numviews = (req.session.numviews || 0) + 1;   <span class="c">// สร้าง/อ่าน/อัปเดต</span></pre>
<ul><li>เข้าถึง <code>req.session.ชื่อ</code> ได้จากทุก route · <b>MemoryStore</b> (ค่า default) ใช้สำหรับ debug/พัฒนา <b>ไม่ใช้บน production</b></li></ul>

<h3>Node.js + MySQL (mysql2)</h3>
<ul><li>ติดตั้ง <code>npm install mysql2</code> · ใช้ MySQL Server + <b>MySQL Workbench</b> จัดการ DB</li>
<li>เตรียม: สร้าง DB/ตาราง (เช่น <code>tinycollege.sql</code>) → สร้าง user (username, password, host=localhost) → กำหนด privilege</li>
<li>SQL พื้นฐาน: <b>SELECT</b> (WHERE, GROUP BY, HAVING, ORDER BY), <b>INSERT</b>, <b>UPDATE</b>, <b>DELETE</b></li></ul>
<pre>const mysql = require('mysql2');
const connection = mysql.createConnection({
  host: process.env.MYSQL_HOST,      user: process.env.MYSQL_USERNAME,
  password: process.env.MYSQL_PASSWORD, database: process.env.MYSQL_DATABASE
});
connection.connect(err => { if (err) throw err; console.log("Connected DB"); });

<span class="c">// SELECT → results คือ array ของแถว</span>
router.get("/cis-courses", (req, res) => {
  const sql = `SELECT course_code, course_name FROM Course WHERE dept_code='CIS'`;
  connection.query(sql, (error, results) => {
    if (error) throw error;
    res.send(results);                          <span class="c">// ส่งเป็น JSON</span>
  });
});
<span class="c">// INSERT → results.affectedRows ; แล้ว res.redirect("/cis-courses")</span></pre>
<p class="tip">สไลด์ใช้ GET เพื่อ INSERT แค่ตัวอย่าง จริง ๆ ควรใช้ <b>POST</b> · mysql2 รองรับ Promise และ async/await</p>
"""

CHEAT = [
 ("รัน Node", "<code>node file.js</code>"),
 ("export / import", "<code>module.exports</code> / <code>require()</code>"),
 ("Sync vs Async", "Sync = blocking ลำดับแน่นอน · Async = ลำดับอาจสลับ"),
 ("ตอบ HTTP", "<code>res.send / sendFile / status().send</code>"),
 ("GET / POST", "<code>req.query</code> / <code>req.body</code> (+urlencoded)"),
 ("Static files", "<code>express.static</code>"),
 ("Cookie", "client · <code>cookie-parser</code> · <code>res.cookie</code>"),
 ("Session", "server · <code>express-session</code> · <code>req.session</code>"),
 ("Env", "<code>.env</code> + <code>dotenv.config()</code> → <code>process.env</code>"),
 ("MySQL", "<code>mysql2</code> · <code>createConnection</code> · <code>query</code>"),
]

PX = [
 ("Node.js ใช้ภาษาโปรแกรมใดในการเขียนโค้ด?", ["JavaScript", "Python", "Java", "C#"], "Node.js คือสภาพแวดล้อมสำหรับรัน JavaScript นอกเบราว์เซอร์"),
 ("ฟังก์ชันใดใช้นำเข้า (import) module ใน Node.js?", ["`require()`", "`module.exports`", "`console.log()`", "`listen()`"], "`require()` = นำเข้า, `module.exports` = ส่งออก"),
 ("`http.createServer()` ใช้ทำอะไร?", ["สร้างเว็บเซิร์ฟเวอร์", "อ่านไฟล์", "เชื่อมต่อฐานข้อมูล", "ติดตั้งแพ็กเกจ"], "`createServer` สร้างเซิร์ฟเวอร์ แล้วใช้ `listen(port)` เปิดรอรับ request"),
 ("Express คืออะไร?", ["Framework สำหรับสร้างเว็บเซิร์ฟเวอร์บน Node.js", "ฐานข้อมูล", "โปรแกรมแก้ไขรูปภาพ", "ภาษาโปรแกรมใหม่"], "Express ช่วยทำ routing และสร้างเว็บ/API ให้ง่ายขึ้น"),
 ("คำสั่ง `npm install express` ทำอะไร?", ["ติดตั้งแพ็กเกจ express ลงในโปรเจกต์", "รันเซิร์ฟเวอร์", "ลบโปรเจกต์", "สร้างไฟล์ HTML"], "npm เป็นตัวจัดการแพ็กเกจของ Node.js"),
 ("ฟอร์มที่ส่งด้วย method GET ข้อมูลจะไปอยู่ที่ใด?", ["ต่อท้าย URL (อ่านด้วย `req.query`)", "ซ่อนใน cookie", "อยู่ในฐานข้อมูลทันที", "ไม่ถูกส่งไปไหน"], "GET ส่งข้อมูลทาง URL หลังเครื่องหมาย `?`"),
 ("สถานะ HTTP 404 หมายความว่าอะไร?", ["ไม่พบหน้าที่ร้องขอ", "สำเร็จ", "เซิร์ฟเวอร์ล่ม", "ไม่มีสิทธิ์เข้าถึง"], "200 = สำเร็จ, 404 = ไม่พบ, 401 = ไม่มีสิทธิ์"),
 ("Cookie ถูกเก็บไว้ที่ใด?", ["ที่เบราว์เซอร์ของผู้ใช้ (client)", "ที่เซิร์ฟเวอร์", "ที่ฐานข้อมูลเท่านั้น", "ที่ router"], "Cookie อยู่ฝั่ง client ส่วน Session อยู่ฝั่ง server"),
 ("Session ถูกเก็บไว้ที่ใด?", ["ที่ฝั่งเซิร์ฟเวอร์ (server)", "ที่เบราว์เซอร์ของผู้ใช้", "ใน URL", "ในไฟล์ CSS"], "Session เก็บฝั่ง server จึงปลอดภัยกว่า cookie"),
 ("แพ็กเกจ `mysql2` ใช้เชื่อมต่อ Node.js กับฐานข้อมูลใด?", ["MySQL", "MongoDB", "Excel", "Firebase"], "`mysql2` เชื่อมต่อ MySQL แล้วใช้ `connection.query()` สั่ง SQL"),
]
F2 = [
 ("Node.js ทำให้เรารันโค้ด JavaScript ได้ที่ใด?", ["นอกเบราว์เซอร์ เช่น ฝั่ง server", "ได้เฉพาะในเบราว์เซอร์", "ได้เฉพาะในไฟล์ CSS", "ได้เฉพาะในฐานข้อมูล"], "Node.js เป็น runtime ที่รัน JavaScript นอกเบราว์เซอร์ จึงใช้เขียนฝั่ง server ได้"),
 ("คำว่า non-blocking หมายถึงอะไร?", ["ไม่ต้องรองานหนึ่งเสร็จก่อนจึงเริ่มงานถัดไป", "ทำงานทีละงานจนเสร็จเท่านั้น", "ห้ามผู้ใช้เข้าเว็บพร้อมกัน", "ปิดกั้นการอ่านไฟล์"], "Node ส่งงาน I/O ออกไปแล้วรับ request ถัดไปทันที ไม่ยืนรอ"),
 ("ทำไม Node.js รองรับผู้ใช้จำนวนมากพร้อมกันได้ดี?", ["เพราะ event loop ไม่ต้องรองาน I/O ให้เสร็จก่อน", "เพราะสร้าง thread ใหม่ให้ทุกคน", "เพราะไม่ต้องใช้เครือข่าย", "เพราะคำนวณเลขได้เร็วที่สุด"], "single thread event loop + non-blocking ทำให้รับ request ได้ต่อเนื่อง"),
 ("`__filename` ให้ค่าอะไร?", ["path เต็มของไฟล์ที่กำลังรัน", "ชื่อโฟลเดอร์อย่างเดียว", "ชื่อผู้ใช้เครื่อง", "เวอร์ชันของ Node.js"], "`__dirname` = โฟลเดอร์ปัจจุบัน, `__filename` = path เต็มของไฟล์"),
 ("ในไฟล์ `hello.js` มีฟังก์ชัน `sayHello` แต่ไม่ได้ใช้ `module.exports` ไฟล์อื่นที่ `require('./hello')` จะเรียก `sayHello` ได้หรือไม่?", ["ไม่ได้ เพราะยังไม่ได้ export ออกมา", "ได้ทันที", "ได้ถ้าเปลี่ยนชื่อไฟล์", "ได้ถ้ารันด้วย nodemon"], "ของในแต่ละ module เป็น private จนกว่าจะส่งออกด้วย `module.exports`"),
 ("`path.extname('app.js')` ได้ผลลัพธ์อะไร?", ["`.js`", "`app`", "`app.js`", "`/`"], "`extname` คืนนามสกุลไฟล์"),
 ("ใน fs module ฟังก์ชัน `fs.unlink()` ใช้ทำอะไร?", ["ลบไฟล์", "อ่านไฟล์", "เปลี่ยนชื่อไฟล์", "สร้างโฟลเดอร์"], "readFile = อ่าน, writeFile = เขียน, appendFile = ต่อท้าย, unlink = ลบ, rename = เปลี่ยนชื่อ"),
 ("ใน callback `function(err, contents)` ของ `fs.readFile` ถ้าอ่านไฟล์สำเร็จ `err` จะเป็นอย่างไร?", ["ไม่มีค่า (null) และ `contents` คือเนื้อหาไฟล์", "เป็นเนื้อหาไฟล์", "เป็นชื่อไฟล์", "เป็นตัวเลข 404"], "จึงต้องเช็ค `if(err)` ก่อน แล้วค่อยใช้ `contents`"),
 ("`res.setHeader('Content-Type', 'text/html')` บอกอะไรกับเบราว์เซอร์?", ["ว่าข้อมูลที่ส่งกลับเป็นหน้า HTML", "ว่าเกิด error", "ว่าให้ลบ cookie", "ว่าให้ปิดเซิร์ฟเวอร์"], "`text/plain` = ข้อความธรรมดา, `text/html` = หน้าเว็บ"),
 ("`res.statusCode = 200` หมายความว่าอะไร?", ["request สำเร็จ (OK)", "ไม่พบหน้า", "ไม่มีสิทธิ์เข้าถึง", "เซิร์ฟเวอร์ปิดอยู่"], "200 = OK, 404 = Not Found, 401 = Unauthorized"),
 ("ทำไมนิยมใช้ Express แทนการเขียนด้วย http module ล้วน?", ["เขียน routing และจัดการ request ได้ง่ายและสั้นกว่า", "เพราะ http module ใช้กับ Node ไม่ได้", "เพราะ Express ไม่ต้องใช้ JavaScript", "เพราะ Express เป็นฐานข้อมูล"], "Express ช่วยเรื่อง routing, API และ template engine"),
 ("npm คืออะไร?", ["ตัวจัดการแพ็กเกจ (package manager) ของ Node.js", "เว็บเบราว์เซอร์", "ฐานข้อมูล", "ภาษาโปรแกรม"], "ใช้ติดตั้ง/ลบแพ็กเกจ และสร้างโปรเจกต์ด้วย `npm init`"),
 ("โฟลเดอร์ `node_modules` เก็บอะไร?", ["แพ็กเกจที่ติดตั้งด้วย npm", "ไฟล์ HTML ของเรา", "รูปภาพของเว็บ", "ข้อมูลในฐานข้อมูล"], "รายการแพ็กเกจอยู่ใน package.json ส่วนตัวไฟล์จริงอยู่ใน node_modules"),
 ("route หนึ่งเส้นใน Express ประกอบด้วยอะไร?", ["HTTP method และ path เช่น GET /shabu", "ชื่อไฟล์และนามสกุล", "IP address และรหัสผ่าน", "cookie และ session"], "เช่น `router.get('/shabu', ...)` = method GET ที่ path /shabu"),
 ("`res.send('Hello')` ทำอะไร?", ["ส่งข้อความ Hello กลับไปที่ client", "พิมพ์ Hello ใน terminal", "บันทึก Hello ลงไฟล์", "ส่งอีเมล"], "ถ้าจะพิมพ์ใน terminal ใช้ `console.log()`"),
 ("`app.listen(3000)` ทำอะไร?", ["เปิดเซิร์ฟเวอร์รอรับ request ที่พอร์ต 3000", "ปิดเซิร์ฟเวอร์ภายใน 3000 วินาที", "ติดตั้ง Express รุ่น 3000", "ส่ง request 3000 ครั้ง"], "จากนั้นเข้าได้ที่ `http://localhost:3000`"),
 ("แอตทริบิวต์ `name` ของ `<input>` ในฟอร์มมีไว้ทำอะไร?", ["เป็นชื่อที่ server ใช้อ่านค่า เช่น `req.body.fname`", "กำหนดสีของช่องกรอก", "กำหนดขนาดตัวอักษร", "ไม่มีผลอะไร"], "`name=\"fname\"` → อ่านด้วย `req.query.fname` (GET) หรือ `req.body.fname` (POST)"),
 ("ถ้าฟอร์มส่งรหัสผ่าน ควรใช้ method ใด?", ["POST เพราะข้อมูลไม่แสดงใน URL", "GET เพราะเร็วกว่า", "GET เพราะเห็นค่าง่าย", "ไม่ต้องใช้ method"], "GET ใส่ข้อมูลต่อท้าย URL ทุกคนจึงมองเห็น"),
 ("ในแท็ก `<form>` แอตทริบิวต์ใดกำหนดว่าจะส่งข้อมูลไปที่ path ไหน?", ["`action`", "`method`", "`name`", "`id`"], "`action` = ปลายทาง, `method` = GET/POST"),
 ("navbar มีลิงก์ `href=\"/shabu\"` แต่ใน app.js ไม่มี route `/shabu` เมื่อกดจะเกิดอะไร?", ["เจอหน้า 404 / Invalid Path", "เปิด shabu.html ได้ปกติ", "เซิร์ฟเวอร์ติดตั้ง route ให้เอง", "เบราว์เซอร์ปิดตัว"], "path ใน href ต้องตรงกับ route ที่กำหนดใน app.js"),
 ("ทำไมเว็บต้องใช้ cookie หรือ session เพื่อจำว่าผู้ใช้ login แล้ว?", ["เพราะ HTTP เป็น stateless จำไม่ได้ว่าใครส่ง request มา", "เพราะ HTTP จำผู้ใช้ได้อยู่แล้ว", "เพราะต้องการให้เว็บช้าลง", "เพราะ Node.js บังคับ"], "แต่ละ request ไม่เกี่ยวกัน จึงต้องมีสิ่งช่วยจำ"),
 ("เมื่อเบราว์เซอร์ได้รับ cookie แล้ว จะทำอะไรกับมัน?", ["เก็บไว้และส่งกลับไปพร้อม request ครั้งต่อไปที่ server เดิม", "ลบทิ้งทันที", "ส่งไปให้ทุกเว็บไซต์", "แปลงเป็นไฟล์ HTML"], "server จึงอ่านได้ด้วย `req.cookies`"),
 ("ข้อใดเป็นตัวอย่างการใช้ cookie ที่ถูกต้อง?", ["จำว่าผู้ใช้ login อยู่", "เก็บรหัสผ่านฐานข้อมูล", "เก็บโค้ด app.js", "เก็บไฟล์รูปภาพ"], "cookie ใช้ทำ session management, personalization, tracking"),
 ("ทำไมไม่ควรอัปโหลดไฟล์ `.env` ขึ้นที่สาธารณะ?", ["เพราะมีข้อมูลลับ เช่น รหัสผ่านฐานข้อมูล", "เพราะไฟล์ใหญ่เกินไป", "เพราะเป็นไฟล์รูปภาพ", "เพราะทำให้โค้ดรันไม่ได้"], ".env เก็บค่าตั้งค่าอย่าง DB_PASSWORD, SESSION_SECRET"),
 ("`process.env.PORT` ได้ค่ามาจากที่ใด?", ["ไฟล์ `.env` หลังเรียก `dotenv.config()`", "ไฟล์ package.json", "ฐานข้อมูล MySQL", "cookie ของผู้ใช้"], "dotenv โหลดค่าใน .env เข้า `process.env`"),
 ("ตั้ง `req.session.username = 'Sam'` ใน route หนึ่ง แล้วไปอีก route จะอ่านค่านี้ได้หรือไม่?", ["ได้ ผ่าน `req.session.username`", "ไม่ได้ ใช้ได้แค่ route เดียว", "ได้เฉพาะใน HTML", "ต้องติดตั้ง mysql2 ก่อน"], "session ใช้ร่วมกันได้ทุก route ในเว็บเดียวกัน"),
 ("ปุ่ม Logout ควรทำอะไรกับ cookie `tokenID`?", ["ลบทิ้งด้วย `res.clearCookie('tokenID')`", "สร้างเพิ่มอีกอัน", "เปลี่ยนเป็น session", "ส่งไปเก็บในฐานข้อมูล"], "เมื่อไม่มี token แล้ว หน้า restrict จะตอบ 401"),
 ("คำสั่ง SQL ใดใช้ดึงข้อมูลออกมาแสดง?", ["SELECT", "INSERT", "DELETE", "UPDATE"], "SELECT = ดึง, INSERT = เพิ่ม, UPDATE = แก้ไข, DELETE = ลบ"),
 ("คำสั่ง SQL ใดใช้เพิ่มข้อมูลแถวใหม่?", ["INSERT", "SELECT", "UPDATE", "WHERE"], "เช่น `INSERT INTO Course VALUES(...)`"),
 ("ข้อใดเรียงลำดับการทำงานของเว็บที่ใช้ฐานข้อมูลได้ถูกต้อง?", ["client ส่ง request → server ส่ง SQL ไป DB → server ส่งผลกลับ client", "DB ส่งข้อมูลไปที่ client โดยตรง", "client ส่ง SQL ไปที่ DB เอง", "server ส่งไฟล์ .env ให้ client"], "client ไม่คุยกับฐานข้อมูลตรง ๆ ต้องผ่าน server"),
]

F3 = [
 ("Node.js สร้างอยู่บน JavaScript engine ตัวใด?", ["V8 ของ Chrome", "SpiderMonkey ของ Firefox", "MySQL", "Express"], "Node.js = JavaScript runtime บน V8 engine"),
 ("คำว่า single thread ใน Node.js หมายถึงอะไร?", ["มี thread หลักตัวเดียวคอยรับ request", "รองรับผู้ใช้ได้ทีละคน", "รันได้แค่ไฟล์เดียว", "ใช้ CPU ได้แค่ครึ่งเดียว"], "thread หลักรับงานแล้วส่งต่อ ไม่ยืนรอ"),
 ("แอปแบบใดเหมาะจะทำด้วย Node.js มากที่สุด?", ["แอปแชตแบบ real-time", "โปรแกรมคำนวณสมการหนัก ๆ", "โปรแกรมตัดต่อวิดีโอ", "เกมกราฟิก 3D"], "เหมาะกับงาน I/O และ real-time ไม่เหมาะกับงานคำนวณหนัก"),
 ("ต้องการใช้ฟังก์ชัน `add` จาก `math.js` ใน `app.js` ต้องทำอย่างไร?", ["`module.exports` ใน math.js แล้ว `require('./math')` ใน app.js", "copy โค้ดไปทุกไฟล์เท่านั้น", "ใช้ `<script>` ใน app.js", "ใช้ `res.send()`"], "export ฝั่งเจ้าของ แล้ว require ฝั่งผู้ใช้"),
 ("`console.log()` ในโปรแกรม Node.js แสดงผลที่ใด?", ["ใน terminal / command line", "ในหน้าเว็บของผู้ใช้", "ในไฟล์ .env", "ในฐานข้อมูล"], "Node ไม่มี window ข้อความจึงออกที่ terminal ที่รันโปรแกรม"),
 ("URL `https://shop.com:8080/item?id=5` มี port เป็นเลขใด?", ["8080", "5", "443", "3000"], "port อยู่หลังเครื่องหมาย `:` ต่อจาก host"),
 ("ส่วน `?id=5` ใน URL เรียกว่าอะไร?", ["query string", "port", "protocol", "pathname"], "อ่านค่าด้วย `searchParams.get('id')` หรือ `req.query.id`"),
 ("ถ้าใช้ `readFileSync` อ่านไฟล์ขนาดใหญ่มากบนเซิร์ฟเวอร์ จะเกิดอะไร?", ["โปรแกรมต้องหยุดรอจนอ่านเสร็จ request อื่นก็ต้องรอ", "อ่านเสร็จทันทีเสมอ", "ไฟล์จะถูกลบ", "ไม่มีผลอะไร"], "Sync = blocking จึงแนะนำให้ใช้แบบ async"),
 ("ใน `http://localhost:8081` คำว่า localhost หมายถึงอะไร?", ["เครื่องคอมพิวเตอร์ของเราเอง", "เซิร์ฟเวอร์ของ Google", "ชื่อฐานข้อมูล", "ชื่อไฟล์ HTML"], "ใช้ทดสอบเซิร์ฟเวอร์ที่รันอยู่บนเครื่องตัวเอง"),
 ("ใน `createServer((req, res) => {...})` ตัว `req` และ `res` คืออะไร?", ["req = สิ่งที่ client ร้องขอ, res = สิ่งที่ server ตอบกลับ", "req = ไฟล์ HTML, res = ไฟล์ CSS", "req = cookie, res = session", "ทั้งคู่คือฐานข้อมูล"], "อ่าน `req.url`, `req.method` และตอบด้วย `res.write()`, `res.end()`"),
 ("ไฟล์ `package.json` มีไว้ทำอะไร?", ["เก็บข้อมูลโปรเจกต์และรายการแพ็กเกจที่ใช้", "เก็บรหัสผ่าน", "เก็บรูปภาพของเว็บ", "เก็บข้อมูลผู้ใช้"], "มีชื่อโปรเจกต์ entry point scripts และ dependencies"),
 ("`const app = express();` ทำอะไร?", ["สร้างแอป Express ขึ้นมาใช้งาน", "ติดตั้ง Express", "ปิดเซิร์ฟเวอร์", "เชื่อมฐานข้อมูล"], "หลังจากนั้นใช้ `app.get()`, `app.use()`, `app.listen()`"),
 ("`app.get('/about', ...)` จะทำงานเมื่อใด?", ["เมื่อผู้ใช้เข้า path /about ด้วย GET", "ทุกครั้งที่เปิดเซิร์ฟเวอร์", "เมื่อส่งฟอร์มด้วย POST ไปที่ /about", "เมื่อผู้ใช้ปิดเบราว์เซอร์"], "method และ path ต้องตรงกันทั้งคู่"),
 ("ทำไมต้องแยก router เป็นหลายโมดูล (เช่น /product, /user)?", ["เมื่อเว็บใหญ่ขึ้น จะจัดระเบียบและดูแลโค้ดง่าย", "เพราะ Express บังคับ", "เพื่อให้เว็บโหลดรูปเร็วขึ้น", "เพื่อเลี่ยงการใช้ npm"], "แต่ละกลุ่มงานมี router ของตัวเอง"),
 ("ข้อใดเป็น static file?", ["ไฟล์ CSS และรูปภาพ", "ข้อมูลจาก SELECT", "ค่าใน req.body", "ค่าใน req.session"], "static file ส่งได้ตรง ๆ ไม่ต้องประมวลผล ใช้ `express.static`"),
 ("กรอก fname=John แล้วกด submit ฟอร์มแบบ GET ที่ `action=\"/form-get\"` URL จะเป็นแบบใด?", ["`/form-get?fname=John`", "`/form-get/John`", "`/John?form-get`", "`/form-get` (ไม่มีค่าใน URL)"], "GET ใส่ค่าต่อท้าย URL หลัง `?`"),
 ("ทำไมฟอร์ม POST ต้องมี `express.urlencoded()`?", ["เพราะข้อมูลอยู่ใน body ต้องแปลงก่อนจึงอ่าน `req.body` ได้", "เพราะ POST ส่งข้อมูลทาง URL", "เพื่อเข้ารหัสรหัสผ่าน", "เพื่อเปิดพอร์ต"], "ถ้าไม่มี middleware นี้ `req.body` จะไม่มีค่า"),
 ("การตรวจสอบข้อมูลที่ผู้ใช้กรอกในฟอร์มควรทำที่ใด?", ["ที่เบราว์เซอร์ และตรวจซ้ำที่ server ถ้าจะบันทึกลงฐานข้อมูล", "ไม่ต้องตรวจเลย", "ตรวจในไฟล์ .env", "ตรวจใน package.json"], "ตรวจฝั่ง client ช่วยผู้ใช้ ตรวจฝั่ง server ป้องกันข้อมูลผิด"),
 ("middleware ทำงานตอนไหน?", ["ระหว่างที่ request เข้ามา ก่อนส่ง response กลับ", "หลังจากปิดเซิร์ฟเวอร์", "ตอนติดตั้งแพ็กเกจ", "ตอนเขียน HTML"], "middleware เข้าถึง req และ res ได้ เช่น `express.json()`"),
 ("`res.sendFile()` ต่างจาก `res.send()` อย่างไร?", ["sendFile ส่งไฟล์ เช่น HTML ส่วน send ส่งข้อความหรือข้อมูล", "เหมือนกันทุกอย่าง", "sendFile ใช้ลบไฟล์", "send ใช้ได้เฉพาะ POST"], "เช่น `res.sendFile(path.join(__dirname, 'html/shabu.html'))`"),
 ("ข้อมูลสำคัญของผู้ใช้ควรเก็บที่ใดจึงปลอดภัยกว่า?", ["Session (ฝั่ง server)", "Cookie (ฝั่ง client)", "ใน URL", "ในไฟล์ HTML"], "cookie ผู้ใช้เปิดอ่านได้ session อยู่ที่ server"),
 ("`res.cookie('theme', 'dark')` สร้าง cookie แบบใด?", ["ชื่อ theme ค่า dark", "ชื่อ dark ค่า theme", "ลบ cookie ชื่อ theme", "สร้าง session ชื่อ dark"], "รูปแบบ `res.cookie(ชื่อ, ค่า)`"),
 ("ผู้ใช้ลบ cookie ในเบราว์เซอร์ทิ้ง แล้วเข้าหน้า `/restrict` ที่ตรวจ cookie จะเกิดอะไร?", ["ถูกปฏิเสธ (401) เพราะไม่มี cookie แล้ว", "เข้าได้ตามปกติ", "server สร้าง cookie คืนให้เอง", "เกิดหน้า 200 ว่าง"], "หน้า restrict ตรวจ `req.cookies` ถ้าไม่มีจะตอบ 401"),
 ("server รู้ได้อย่างไรว่า session ไหนเป็นของผู้ใช้คนใด?", ["ใช้ session ID ที่ส่งมากับ cookie ในแต่ละ request", "ดูจากชื่อเบราว์เซอร์", "ดูจากสีหน้าจอ", "ถามผู้ใช้ทุกครั้ง"], "cookie ช่วยให้แต่ละ request มีตัวระบุผู้ใช้ จึงทำ session ได้"),
 ("ถ้า restart เซิร์ฟเวอร์ที่ใช้ MemoryStore เก็บ session ค่าใน session จะเป็นอย่างไร?", ["หายหมด ต้องเริ่มใหม่", "อยู่ครบเหมือนเดิม", "ย้ายไปอยู่ใน cookie", "ถูกบันทึกลง MySQL อัตโนมัติ"], "MemoryStore เก็บในหน่วยความจำ จึงเหมาะแค่ตอนพัฒนา"),
 ("ทำไมต้องสร้างบัญชีผู้ใช้ฐานข้อมูลและกำหนดสิทธิ์ (privilege) ก่อนเชื่อมต่อจาก Node.js?", ["ให้ Node.js ใช้บัญชีนั้นเชื่อมต่อ และทำได้เฉพาะคำสั่งที่อนุญาต", "เพื่อให้ผู้ใช้เว็บเห็นรหัสผ่าน", "เพื่อให้ไม่ต้องใช้ SQL", "เพราะ npm บังคับ"], "ตั้ง username, password, host และสิทธิ์ใน MySQL Workbench"),
 ("MySQL Workbench ใช้ทำอะไร?", ["จัดการฐานข้อมูล MySQL ผ่านหน้าจอ GUI", "เขียนโค้ด Node.js", "ติดตั้ง Express", "เปิดเว็บไซต์"], "ใช้สร้าง DB ตาราง และผู้ใช้ฐานข้อมูล"),
 ("ผล `results` ของคำสั่ง SELECT ใน `connection.query()` มีลักษณะอย่างไร?", ["array ของแถวข้อมูล", "ข้อความ OK", "ตัวเลข 200", "ไฟล์ HTML"], "ส่งกลับด้วย `res.send(results)` จะได้ JSON"),
 ("หลัง INSERT สำเร็จแล้วเรียก `res.redirect('/cis-courses')` จะเกิดอะไร?", ["พาผู้ใช้ไปหน้าแสดงรายวิชาทั้งหมด", "ลบข้อมูลที่เพิ่งเพิ่ม", "ปิดการเชื่อมต่อฐานข้อมูล", "สร้าง cookie ใหม่"], "redirect = ส่งผู้ใช้ไปอีก path"),
 ("คำสั่ง SQL `UPDATE` ใช้ทำอะไร?", ["แก้ไขข้อมูลที่มีอยู่แล้ว", "เพิ่มแถวใหม่", "ดึงข้อมูล", "ลบตาราง"], "SELECT ดึง, INSERT เพิ่ม, UPDATE แก้, DELETE ลบ"),
]
# ซ้อมสอบ 2-6: 20 ข้อ/ชุด ง่าย ตรงตัว  ข้อ 1-7 = L9, 8-14 = L10, 15-20 = L11
Z1 = [
 ("Node.js คืออะไร?", ["สภาพแวดล้อมสำหรับรัน JavaScript นอกเบราว์เซอร์", "ภาษาโปรแกรมใหม่ที่ไม่ใช่ JavaScript", "โปรแกรมสร้างฐานข้อมูล", "เว็บเบราว์เซอร์ตัวหนึ่ง"], "Node.js เป็น JavaScript runtime ไม่ใช่ภาษาใหม่"),
 ("ใช้คำสั่งใดตรวจว่าติดตั้ง Node.js เวอร์ชันอะไร?", ["`node --version`", "`npm start`", "`node app.js`", "`npm init`"], "`node --version` แสดงเวอร์ชันที่ติดตั้ง"),
 ("โค้ดที่รันในเบราว์เซอร์ของผู้ใช้ เรียกว่าอะไร?", ["Client-side", "Server-side", "Database-side", "Router-side"], "HTML, CSS, JS ในเบราว์เซอร์ = client-side ส่วน Node.js = server-side"),
 ("Node.js ไม่ต้องรองานอ่านไฟล์หรือฐานข้อมูลให้เสร็จ แต่รับ request ถัดไปได้เลย เรียกว่าอะไร?", ["non-blocking", "blocking", "hardcode", "debugging"], "non-blocking = ไม่ยืนรอ ทำให้รับผู้ใช้ได้ต่อเนื่อง"),
 ("`module.exports` ใช้ทำอะไร?", ["ส่งออกฟังก์ชันหรือค่าจากไฟล์ ให้ไฟล์อื่นใช้", "นำเข้าไฟล์อื่นมาใช้", "ลบไฟล์", "เปิดเซิร์ฟเวอร์"], "`module.exports` = ส่งออก, `require()` = นำเข้า"),
 ("`require()` ใช้ทำอะไร?", ["นำเข้า module มาใช้", "ส่งออก module", "สร้างฐานข้อมูล", "ลบ cookie"], "เช่น `const http = require('http')`"),
 ("`res.statusCode = 200` หมายถึงอะไร?", ["สำเร็จ (OK)", "ไม่พบหน้า", "ไม่มีสิทธิ์เข้าถึง", "เซิร์ฟเวอร์ล่ม"], "200 = OK, 404 = ไม่พบ, 401 = ไม่มีสิทธิ์"),
 ("Express คืออะไร?", ["Framework ช่วยสร้างเว็บเซิร์ฟเวอร์บน Node.js", "ฐานข้อมูล", "ภาษาโปรแกรม", "โปรแกรมตกแต่งรูป"], "Express ช่วยทำ routing และ API ให้ง่ายขึ้น"),
 ("`npm init` ทำอะไร?", ["สร้างโปรเจกต์ใหม่และไฟล์ package.json", "รันเซิร์ฟเวอร์", "ลบโปรเจกต์", "ติดตั้ง Express"], "`npm init` ถามข้อมูลทีละข้อ แล้วสร้าง package.json"),
 ("nodemon ช่วยอะไร?", ["restart เซิร์ฟเวอร์ให้อัตโนมัติเมื่อแก้ไฟล์", "เข้ารหัสรหัสผ่าน", "เชื่อมฐานข้อมูล", "ส่งอีเมล"], "ไม่ต้องกด Ctrl+C แล้วรันใหม่เองทุกครั้ง"),
 ("`app.get('/', ...)` คือการกำหนดอะไร?", ["route สำหรับ GET ที่ path /", "การติดตั้งแพ็กเกจ", "การเชื่อมฐานข้อมูล", "การลบ cookie"], "route = HTTP method + path"),
 ("`res.send('Hello')` ทำอะไร?", ["ส่งข้อความ Hello กลับไปให้ผู้ใช้", "พิมพ์ Hello ใน terminal", "บันทึก Hello ลงไฟล์", "ส่งอีเมล"], "พิมพ์ใน terminal ใช้ `console.log()`"),
 ("ฟอร์มแบบ GET ข้อมูลที่กรอกจะอ่านด้วยอะไร?", ["`req.query`", "`req.body`", "`req.session`", "`req.cookies`"], "GET → `req.query`, POST → `req.body`"),
 ("ฟอร์มแบบ POST ข้อมูลที่กรอกจะอ่านด้วยอะไร?", ["`req.body`", "`req.query`", "`req.url`", "`req.cookies`"], "POST ส่งข้อมูลใน message body"),
 (".env คือไฟล์อะไร?", ["ไฟล์เก็บค่าตั้งค่าแบบ key=value เช่น PORT", "ไฟล์รูปภาพ", "ไฟล์ HTML หน้าแรก", "ไฟล์ฐานข้อมูล"], "เก็บค่าที่ไม่อยากเขียนตรง ๆ ในโค้ด เช่น PORT, รหัสผ่าน DB"),
 ("HTTP เป็น stateless หมายความว่าอย่างไร?", ["แต่ละ request ไม่เกี่ยวข้องกัน เซิร์ฟเวอร์ไม่จำว่าใครเป็นใคร", "เซิร์ฟเวอร์จำผู้ใช้ทุกคนได้เอง", "ส่งข้อมูลได้ครั้งเดียว", "ใช้ได้เฉพาะกับ Node.js"], "จึงต้องมี cookie/session ช่วยจำผู้ใช้"),
 ("`res.cookie('tokenID', 'abc')` ทำอะไร?", ["สร้าง cookie ชื่อ tokenID", "ลบ cookie", "อ่านค่า cookie", "สร้างตารางในฐานข้อมูล"], "รูปแบบ `res.cookie(ชื่อ, ค่า)`"),
 ("ต้องการลบ cookie ตอน logout ใช้อะไร?", ["`res.clearCookie()`", "`res.cookie()`", "`req.cookies`", "`res.send()`"], "`clearCookie('ชื่อ')` ลบ cookie ออก"),
 ("`req.session.username = 'Sam'` ทำอะไร?", ["เก็บค่า username ไว้ใน session ที่ฝั่งเซิร์ฟเวอร์", "เก็บค่าไว้ในไฟล์ .env", "ลบ session", "เปลี่ยนชื่อไฟล์"], "อ่านค่านี้ได้จากทุก route"),
 ("คำสั่ง SQL `DELETE` ทำอะไร?", ["ลบข้อมูล", "เพิ่มข้อมูล", "ดึงข้อมูล", "แก้ไขข้อมูล"], "SELECT ดึง, INSERT เพิ่ม, UPDATE แก้, DELETE ลบ"),
]

Z2 = [
 ("Node.js สร้างอยู่บน JavaScript engine ตัวใด?", ["V8 ของ Chrome", "SpiderMonkey ของ Firefox", "MySQL", "Express"], "Node.js = JavaScript runtime บน V8 engine"),
 ("รันไฟล์ `app.js` ด้วยคำสั่งใด?", ["`node app.js`", "`npm app.js`", "`run app.js`", "`express app.js`"], "รูปแบบ `node ชื่อไฟล์.js`"),
 ("Node.js มี `document` และ `window` แบบในเบราว์เซอร์หรือไม่?", ["ไม่มี", "มีทั้งสองอย่าง", "มีเฉพาะ window", "มีเฉพาะ document"], "Node.js ไม่มี DOM จึงไม่มี document / window"),
 ("งานแบบใดที่ Node.js เหมาะที่สุด?", ["งานรับส่งข้อมูลจำนวนมาก เช่น แชตแบบ real-time", "งานคำนวณคณิตศาสตร์หนัก ๆ", "งานตัดต่อวิดีโอ", "เกม 3D"], "เหมาะกับ I/O หนักและ real-time"),
 ("`require('./hello')` เครื่องหมาย `./` หมายถึงอะไร?", ["ไฟล์ของเราเองในโฟลเดอร์ปัจจุบัน", "โฟลเดอร์ของ Node.js", "แพ็กเกจจาก npm", "ไฟล์ในอินเทอร์เน็ต"], "ไฟล์ของเราเองต้องใช้ `./` นำหน้า"),
 ("`fs` module ใช้ทำอะไร?", ["จัดการไฟล์ เช่น อ่าน เขียน ลบ", "สร้างเซิร์ฟเวอร์", "แยกส่วนของ URL", "จัดการ cookie"], "fs = file system"),
 ("ต้องการสร้างเว็บเซิร์ฟเวอร์ด้วย Node.js เปล่า ๆ (ไม่ใช้ Express) ใช้ module ใด?", ["`http`", "`fs`", "`path`", "`url`"], "`http.createServer()` แล้ว `listen(port)`"),
 ("Express ช่วยเรื่องอะไรเป็นหลัก?", ["routing และการสร้างเว็บ/API", "วาดกราฟิก", "เล่นเสียง", "บีบอัดไฟล์"], "นอกจากนี้ใช้ร่วมกับ template engine ได้"),
 ("`npm init -y` ต่างจาก `npm init` อย่างไร?", ["ข้ามคำถาม ใช้ค่า default ให้เลย", "ลบโปรเจกต์", "ติดตั้ง Express", "รันเซิร์ฟเวอร์"], "`-y` = yes กับทุกคำถาม"),
 ("หลัง clone โปรเจกต์มา ใช้ `npm install` เฉย ๆ (ไม่ใส่ชื่อ) เพื่ออะไร?", ["ติดตั้งแพ็กเกจทั้งหมดที่อยู่ใน package.json", "ลบ node_modules", "สร้างไฟล์ app.js", "เปิดเซิร์ฟเวอร์"], "อ่านรายการ dependencies จาก package.json แล้วลงให้ครบ"),
 ("`const app = express();` ทำอะไร?", ["สร้างแอป Express", "ติดตั้ง Express", "ปิดเซิร์ฟเวอร์", "เชื่อมต่อ MySQL"], "หลังจากนั้นใช้ `app.get()`, `app.listen()`"),
 ("ใน `app.listen(port, callback)` ส่วน port คืออะไร?", ["หมายเลขช่องทางที่เซิร์ฟเวอร์รอรับ request", "ชื่อไฟล์", "ชื่อผู้ใช้ฐานข้อมูล", "รหัสผ่าน"], "พอร์ตที่เจอบ่อย: 3000, 8080, 8081"),
 ("ไฟล์ CSS และรูปภาพที่ส่งให้ผู้ใช้ตรง ๆ ใช้ตัวใดให้บริการ?", ["`express.static`", "`express.json`", "`express.Router`", "`res.cookie`"], "static file ไม่ต้องประมวลผล ส่งไฟล์ไปได้เลย"),
 ("ในแท็ก `<form>` แอตทริบิวต์ `action` กำหนดอะไร?", ["path ปลายทางที่จะส่งข้อมูลไป", "สีของปุ่ม", "ขนาดตัวอักษร", "ชื่อไฟล์ CSS"], "`action` = ปลายทาง, `method` = GET/POST"),
 ("ติดตั้งแพ็กเกจ dotenv ด้วยคำสั่งใด?", ["`npm install dotenv`", "`node dotenv`", "`npm start dotenv`", "`express dotenv`"], "รูปแบบ `npm install <ชื่อแพ็กเกจ>`"),
 ("`dotenv.config()` ทำอะไร?", ["โหลดค่าจากไฟล์ .env เข้ามาใช้", "ลบไฟล์ .env", "เปิดเซิร์ฟเวอร์", "สร้างฐานข้อมูล"], "หลังโหลดแล้วอ่านด้วย `process.env.ชื่อ`"),
 ("Cookie ถูกเก็บไว้ที่ใด?", ["ที่เบราว์เซอร์ของผู้ใช้ (client)", "ที่เซิร์ฟเวอร์", "ในฐานข้อมูลเท่านั้น", "ในไฟล์ app.js"], "Cookie อยู่ฝั่ง client ส่วน Session อยู่ฝั่ง server"),
 ("`req.cookies` ใช้ทำอะไร?", ["อ่านค่า cookie ที่เบราว์เซอร์ส่งมา", "สร้าง cookie", "ลบ cookie", "อ่านค่า session"], "ต้องใช้ `cookie-parser` ก่อน จึงจะอ่านได้"),
 ("แพ็กเกจ `mysql2` ใช้ทำอะไร?", ["เชื่อมต่อ Node.js กับ MySQL", "สร้างหน้าเว็บ", "จัดการ cookie", "ส่งอีเมล"], "ใช้ `connection.query()` ส่ง SQL"),
 ("คำสั่ง SQL ใดใช้ดึงข้อมูล?", ["SELECT", "INSERT", "UPDATE", "DELETE"], "SELECT = ดึงข้อมูลมาแสดง"),
]

Z3 = [
 ("Server-side คืออะไร?", ["โค้ดที่รันบนเซิร์ฟเวอร์ แล้วเลือกว่าจะส่งอะไรกลับไปให้ผู้ใช้", "โค้ดที่รันในเบราว์เซอร์ของผู้ใช้", "ไฟล์รูปภาพ", "สีของหน้าเว็บ"], "Node.js, PHP, Python เป็นตัวอย่างของ server-side"),
 ("`console.log('Hi')` ใน Node.js จะแสดง Hi ที่ใด?", ["ใน terminal ที่รันโปรแกรม", "ในหน้าเว็บ", "ในไฟล์ .env", "ในฐานข้อมูล"], "Node.js ไม่มี window ข้อความจึงออกที่ terminal"),
 ("งานแบบใดที่ Node.js ไม่เหมาะ?", ["งานคำนวณหนัก ๆ ที่ใช้ CPU มาก", "แอปแชต", "JSON API", "งานอ่าน/เขียนข้อมูลจำนวนมาก"], "Node.js เป็น single thread งานคำนวณหนักจะทำให้ทุกคนต้องรอ"),
 ("`__dirname` คืออะไร?", ["path ของโฟลเดอร์ที่ไฟล์นั้นอยู่", "ชื่อผู้ใช้เครื่อง", "เวอร์ชัน Node.js", "ชื่อฐานข้อมูล"], "ใช้ได้ทุกไฟล์โดยไม่ต้อง require"),
 ("`path` module ใช้ทำอะไร?", ["จัดการที่อยู่ไฟล์ (path) ให้เหมาะกับแต่ละระบบปฏิบัติการ", "สร้างเว็บเซิร์ฟเวอร์", "อ่านไฟล์", "เชื่อมฐานข้อมูล"], "เช่น `path.join()`, `path.extname()`"),
 ("`fs.writeFile()` ใช้ทำอะไร?", ["เขียนข้อมูลลงไฟล์", "อ่านไฟล์", "ลบไฟล์", "เปิดเซิร์ฟเวอร์"], "readFile = อ่าน, writeFile = เขียน, appendFile = ต่อท้าย"),
 ("`server.listen(8081)` ทำอะไร?", ["ให้เซิร์ฟเวอร์รอรับ request ที่พอร์ต 8081", "ปิดเซิร์ฟเวอร์", "อ่านไฟล์ 8081 ไฟล์", "ติดตั้งแพ็กเกจ"], "จากนั้นเปิด `http://localhost:8081` ได้"),
 ("template engine เช่น Pug, EJS ใช้ทำอะไร?", ["แทนตัวแปรในไฟล์ template ด้วยค่าจริงแล้วสร้างเป็นหน้า HTML", "เข้ารหัสรหัสผ่าน", "เชื่อมต่อฐานข้อมูล", "ติดตั้งแพ็กเกจ"], "ทำให้หน้าเว็บเปลี่ยนตามข้อมูลได้ (dynamic)"),
 ("npm คืออะไร?", ["ตัวจัดการแพ็กเกจของ Node.js", "เว็บเบราว์เซอร์", "ฐานข้อมูล", "ไฟล์ตั้งค่า"], "npm = Node Package Manager"),
 ("ถ้าไม่ใช้แพ็กเกจนั้นแล้ว ต้องการเอาออก ใช้คำสั่งใด?", ["`npm uninstall <ชื่อแพ็กเกจ>`", "`npm install <ชื่อแพ็กเกจ>`", "`npm init`", "`npm start`"], "install = ติดตั้ง, uninstall = ถอนออก"),
 ("ไฟล์ `package.json` เก็บอะไร?", ["ข้อมูลโปรเจกต์และรายการแพ็กเกจที่ใช้", "รหัสผ่านผู้ใช้", "รูปภาพ", "ข้อมูลในฐานข้อมูล"], "มีชื่อโปรเจกต์ entry point scripts และ dependencies"),
 ("`res.sendFile()` ใช้ทำอะไร?", ["ส่งไฟล์ เช่น หน้า HTML กลับไปให้ผู้ใช้", "ลบไฟล์", "สร้างไฟล์ใหม่", "เปลี่ยนชื่อไฟล์"], "เช่น ส่ง `shabu.html` ตอนเข้า /shabu"),
 ("route ที่ดักเส้นทางซึ่งไม่มี route ไหนรับ (ตอบ 404) ควรวางไว้ตรงไหน?", ["ท้ายสุดของ routes ทั้งหมด", "บนสุดของไฟล์", "ในไฟล์ .env", "ไม่ต้องวาง"], "ถ้าวางไว้ก่อน มันจะดักทุก path ไปหมด route อื่นจะไม่ได้ทำงาน"),
 ("ฟอร์มที่ใช้ method POST ส่งข้อมูลไปที่ใด?", ["ใน message body ของ request", "ต่อท้าย URL", "ใน cookie", "ในไฟล์ CSS"], "GET = ต่อท้าย URL, POST = ใน body"),
 ("ในโค้ดอ่านค่า PORT ที่เก็บไว้ใน .env ใช้อะไร?", ["`process.env.PORT`", "`req.env.PORT`", "`dotenv.PORT`", "`res.PORT`"], "หลังเรียก `dotenv.config()`"),
 ("Session ถูกเก็บไว้ที่ใด?", ["ที่เซิร์ฟเวอร์", "ที่เบราว์เซอร์ของผู้ใช้", "ใน URL", "ในไฟล์ CSS"], "จึงปลอดภัยกว่า cookie"),
 ("แพ็กเกจใดใช้จัดการ session ใน Express?", ["`express-session`", "`cookie-parser`", "`mysql2`", "`dotenv`"], "`cookie-parser` ใช้อ่าน cookie"),
 ("`maxAge` ของ cookie ใช้กำหนดอะไร?", ["อายุของ cookie (หน่วยมิลลิวินาที)", "ขนาดของ cookie", "ชื่อของ cookie", "สีของ cookie"], "เช่น `{ maxAge: 360000 }`"),
 ("MySQL Workbench ใช้ทำอะไร?", ["จัดการฐานข้อมูล MySQL ผ่านหน้าจอ", "เขียนโค้ด Node.js", "ติดตั้ง Express", "เปิดเว็บเบราว์เซอร์"], "ใช้สร้างฐานข้อมูล ตาราง และผู้ใช้"),
 ("คำสั่ง SQL ใดใช้เพิ่มข้อมูลแถวใหม่?", ["INSERT", "SELECT", "DELETE", "UPDATE"], "INSERT = เพิ่ม"),
]

Z4 = [
 ("`__filename` ให้ค่าอะไร?", ["path เต็มของไฟล์ที่กำลังรัน", "ชื่อโฟลเดอร์", "ชื่อผู้ใช้", "เวอร์ชัน Node.js"], "`__dirname` = โฟลเดอร์, `__filename` = ไฟล์"),
 ("ใน Node.js ไฟล์ JavaScript 1 ไฟล์ถือเป็นอะไร?", ["1 module", "1 โปรเจกต์", "1 ฐานข้อมูล", "1 เซิร์ฟเวอร์"], "ตัวแปรในไฟล์เป็น private ชื่อซ้ำข้ามไฟล์ไม่ทับกัน"),
 ("`path.extname('photo.png')` ให้ผลลัพธ์อะไร?", ["`.png`", "`photo`", "`photo.png`", "`/`"], "`extname` คืนนามสกุลไฟล์"),
 ("ใน fs module ฟังก์ชัน `unlink` ทำอะไร?", ["ลบไฟล์", "อ่านไฟล์", "เขียนไฟล์", "ต่อท้ายไฟล์"], "unlink = ลบ, rename = เปลี่ยนชื่อ"),
 ("`readFileSync` เป็นการอ่านไฟล์แบบใด?", ["Sync: รอจนอ่านเสร็จก่อนทำบรรทัดต่อไป", "Async: ไม่รอ", "อ่านเฉพาะบรรทัดแรก", "อ่านจากอินเทอร์เน็ต"], "Sync = blocking ลำดับแน่นอน แต่หยุดงานอื่นไว้"),
 ("ใน `createServer((req, res) => ...)` `req.url` คืออะไร?", ["path ที่ผู้ใช้ร้องขอ เช่น /shabu", "ข้อความที่จะตอบกลับ", "ชื่อไฟล์", "รหัสสถานะ"], "`req` = สิ่งที่ขอมา, `res` = สิ่งที่ตอบกลับ"),
 ("`res.setHeader('Content-Type', 'text/html')` บอกเบราว์เซอร์ว่าอะไร?", ["สิ่งที่ส่งกลับไปเป็นหน้า HTML", "เกิด error", "ให้ลบ cookie", "ให้ปิดเซิร์ฟเวอร์"], "`text/plain` = ข้อความธรรมดา"),
 ("โฟลเดอร์ `node_modules` เก็บอะไร?", ["แพ็กเกจที่ติดตั้งด้วย npm", "ไฟล์ HTML", "รูปภาพ", "ข้อมูลผู้ใช้"], "ตัวไฟล์แพ็กเกจอยู่ที่นี่ รายชื่ออยู่ใน package.json"),
 ("ไฟล์ `app.js` ในโปรเจกต์ Express มักทำหน้าที่อะไร?", ["เป็นไฟล์หลัก มี routes และตั้งค่าเซิร์ฟเวอร์", "เก็บรูปภาพ", "เก็บรหัสผ่าน", "เป็นฐานข้อมูล"], "รันด้วย `node app.js` หรือ `npm start`"),
 ("ถ้าตั้ง `\"start\": \"nodemon app.js\"` ใน scripts จะรันโปรเจกต์ด้วยคำสั่งใด?", ["`npm start`", "`npm init`", "`npm install`", "`npm uninstall`"], "scripts ใน package.json เรียกใช้ด้วย `npm start`"),
 ("`express.Router()` ใช้ทำอะไร?", ["สร้างตัวจัดการ route แยกเป็นกลุ่ม", "เชื่อมต่อฐานข้อมูล", "สร้าง cookie", "ลบไฟล์"], "ช่วยแยก routes ให้โค้ดไม่รกใน app.js"),
 ("middleware คืออะไร?", ["ฟังก์ชันที่เข้าถึง req และ res ระหว่างที่ request ผ่านเข้ามา", "ฐานข้อมูล", "ไฟล์ CSS", "ชื่อโฟลเดอร์"], "เช่น `express.json()`, `cookie-parser`"),
 ("แอตทริบิวต์ `name` ของ `<input>` สำคัญอย่างไร?", ["server ใช้ชื่อนี้อ่านค่าที่ผู้ใช้กรอก", "กำหนดสีช่องกรอก", "กำหนดขนาดช่อง", "ไม่มีผลอะไร"], "`name=\"fname\"` → `req.query.fname` หรือ `req.body.fname`"),
 ("ถ้าฟอร์มส่งรหัสผ่าน ไม่ควรใช้ GET เพราะอะไร?", ["ข้อมูลจะไปแสดงใน URL ใครก็มองเห็น", "GET ช้าเกินไป", "GET ใช้ไม่ได้กับ Node.js", "GET ส่งข้อมูลไม่ได้"], "ควรใช้ POST"),
 ("ทำไมไม่ควรอัปโหลดไฟล์ `.env` ขึ้นที่สาธารณะ เช่น GitHub?", ["เพราะมีข้อมูลลับ เช่น รหัสผ่านฐานข้อมูล", "เพราะไฟล์ใหญ่", "เพราะรันไม่ได้", "เพราะเป็นรูปภาพ"], ".env เก็บ DB_PASSWORD, SESSION_SECRET ฯลฯ"),
 ("แพ็กเกจ `cookie-parser` ใช้ทำอะไร?", ["ช่วยให้อ่านค่า cookie ผ่าน `req.cookies` ได้", "จัดการ session", "เชื่อมฐานข้อมูล", "สร้างเซิร์ฟเวอร์"], "ต้องใช้ก่อนอ่าน `req.cookies`"),
 ("เซิร์ฟเวอร์ส่ง cookie ให้เบราว์เซอร์ผ่าน HTTP header ชื่ออะไร?", ["`Set-Cookie`", "`Get-Cookie`", "`Send-Cookie`", "`Cookie-Server`"], "เบราว์เซอร์เก็บไว้ แล้วส่งกลับใน header `Cookie` ทุก request"),
 ("MemoryStore ที่เป็นค่า default ของ session เหมาะกับงานแบบใด?", ["ช่วงพัฒนา/ทดสอบ ไม่ควรใช้บน production", "ใช้งานจริงบน production", "เก็บรูปภาพ", "เก็บ cookie"], "เก็บใน memory ของเซิร์ฟเวอร์ restart แล้วหาย"),
 ("`connection.query(sql, callback)` ทำอะไร?", ["ส่งคำสั่ง SQL ไปให้ฐานข้อมูลทำงาน", "สร้างไฟล์ .env", "ปิดเซิร์ฟเวอร์", "ลบ cookie"], "callback รับ `(error, results)`"),
 ("คำสั่ง SQL `UPDATE` ทำอะไร?", ["แก้ไขข้อมูลที่มีอยู่แล้ว", "เพิ่มแถวใหม่", "ลบตาราง", "ดึงข้อมูล"], "UPDATE = แก้ไข"),
]

Z5 = [
 ("`url` module ใช้ทำอะไร?", ["แยกส่วนต่าง ๆ ของ URL เช่น host, port, pathname", "สร้างเซิร์ฟเวอร์", "อ่านไฟล์", "ลบไฟล์"], "`new URL(str)` แล้วดู `.host` `.port` `.pathname`"),
 ("การอ่านไฟล์แบบ Async (ใช้ callback) ต่างจาก Sync อย่างไร?", ["ไม่ต้องรอ ทำงานอื่นต่อได้ แต่ลำดับผลลัพธ์อาจสลับกัน", "รอจนเสร็จก่อนเสมอ", "อ่านได้เฉพาะไฟล์เล็ก", "ใช้ไม่ได้ใน Node.js"], "Async = non-blocking"),
 ("การเขียน callback ซ้อนกันหลายชั้นจนอ่านยาก เรียกว่าอะไร?", ["Callback Hell", "Event Loop", "Middleware", "Hardcode"], "ซ้อนเป็นขั้นบันได `})` อ่านและดูแลยาก"),
 ("สิ่งใดช่วยแก้ปัญหา callback hell?", ["Promise และ async/await", "เพิ่ม callback ให้มากขึ้น", "ลบ error handling", "ใช้ Sync ทุกที่โดยไม่คิด"], "Promise / async-await ทำให้โค้ดอ่านเป็นลำดับตรง ๆ"),
 ("`res.end()` ทำอะไร?", ["จบการตอบกลับ ส่ง response ให้ผู้ใช้เสร็จ", "ปิดโปรแกรม Node.js", "ลบไฟล์", "ปิดฐานข้อมูล"], "ถ้าไม่เรียก เบราว์เซอร์จะรอตอบกลับค้างอยู่"),
 ("`localhost` หมายถึงอะไร?", ["เครื่องคอมพิวเตอร์ของเราเอง", "เซิร์ฟเวอร์ของ Google", "ชื่อไฟล์ HTML", "ชื่อฐานข้อมูล"], "ใช้ทดสอบเซิร์ฟเวอร์ที่รันบนเครื่องตัวเอง"),
 ("หยุดเซิร์ฟเวอร์ Node.js ที่รันอยู่ใน terminal ด้วยปุ่มอะไร?", ["Ctrl+C", "Ctrl+V", "Ctrl+S", "Ctrl+Z"], "Ctrl+C = หยุดโปรแกรมที่กำลังรัน"),
 ("ติดตั้ง Express ด้วยคำสั่งใด?", ["`npm install express`", "`node express`", "`npm init express`", "`npm start express`"], "ติดตั้งแล้วจะถูกเพิ่มใน dependencies ของ package.json"),
 ("`app.use(router)` ทำอะไร?", ["ลงทะเบียน router ให้แอปใช้งาน", "ลบ router", "เปิดพอร์ต", "สร้างฐานข้อมูล"], "ถ้าไม่ลงทะเบียน routes ใน router จะไม่ทำงาน"),
 ("route หนึ่งเส้นประกอบด้วยอะไร?", ["HTTP method และ path เช่น GET /shabu", "ชื่อไฟล์และนามสกุล", "รหัสผ่านและ cookie", "IP และ port"], "เช่น `POST /user/add`"),
 ("ใน HTML ต้องการใช้ไฟล์ `mystyle.css` ที่อยู่ในโฟลเดอร์ static ควรเขียน `href` อย่างไร?", ["`/mystyle.css`", "`../public/mystyle.css`", "`C:/public/mystyle.css`", "`http://mystyle`"], "โฟลเดอร์ static ถือเป็น root ของ path"),
 ("`app.use('/product', router1)` และใน router1 มี `get('/add')` URL เต็มคืออะไร?", ["`/product/add`", "`/add/product`", "`/add`", "`/product`"], "path ที่ mount + path ใน router = URL เต็ม"),
 ("ฟอร์ม POST ต้องใช้ `express.urlencoded()` เพราะอะไร?", ["เพื่อให้อ่านข้อมูลจากฟอร์มผ่าน `req.body` ได้", "เพื่อเข้ารหัสรหัสผ่าน", "เพื่อเปิดพอร์ต", "เพื่อลบ cookie"], "ถ้าไม่มี `req.body` จะไม่มีค่า"),
 ("ควรตรวจสอบข้อมูลที่ผู้ใช้กรอกในฟอร์มที่ใด?", ["ที่เบราว์เซอร์ และตรวจซ้ำที่เซิร์ฟเวอร์", "ไม่ต้องตรวจเลย", "ที่ไฟล์ .env", "ที่ฐานข้อมูลเท่านั้น"], "ตรวจที่เบราว์เซอร์ช่วยผู้ใช้ ตรวจที่ server ป้องกันข้อมูลผิดก่อนลง DB"),
 ("หน้า `/restrict` ตรวจ cookie ถ้าผู้ใช้ไม่มี cookie ควรตอบสถานะใด?", ["401 (ไม่มีสิทธิ์เข้าถึง)", "200 (สำเร็จ)", "404 (ไม่พบหน้า)", "500 (เซิร์ฟเวอร์พัง)"], "401 = Unauthorized"),
 ("ในการตั้งค่า session ตัว `secret` ใช้ทำอะไร?", ["ใช้ลงนาม (sign) session ID", "เก็บรหัสผ่านผู้ใช้", "เป็นชื่อฐานข้อมูล", "เป็นหมายเลขพอร์ต"], "ค่า secret มักเก็บใน .env เช่น `SESSION_SECRET`"),
 ("`mysql.createConnection({...})` ใช้ใส่ค่าอะไรบ้าง?", ["host, user, password, database ของฐานข้อมูล", "ชื่อไฟล์ HTML", "สีและฟอนต์", "ชื่อ cookie"], "ค่าเหล่านี้มักอ่านจาก `process.env`"),
 ("ผล `results` ที่ได้จากคำสั่ง SELECT มีลักษณะอย่างไร?", ["array ของแถวข้อมูล", "ตัวเลขตัวเดียว", "ไฟล์ HTML", "ข้อความ OK"], "ส่งกลับด้วย `res.send(results)` จะได้ JSON"),
 ("ใน SQL `WHERE` ใช้ทำอะไร?", ["กำหนดเงื่อนไขกรองแถวข้อมูล", "เรียงลำดับข้อมูล", "สร้างตาราง", "ลบฐานข้อมูล"], "เช่น `WHERE dept_code='CIS'`"),
 ("ทำไมไม่ควรเก็บข้อมูลลับ เช่น รหัสผ่าน ไว้ใน cookie?", ["เพราะผู้ใช้เปิดอ่าน cookie ในเบราว์เซอร์ได้", "เพราะ cookie ใหญ่เกินไป", "เพราะ cookie ใช้กับ Node.js ไม่ได้", "เพราะ cookie ลบไม่ได้"], "cookie อยู่ฝั่ง client ข้อมูลลับควรอยู่ใน session ที่ server"),
]

# ---------- ตัวสร้างข้อสอบ ----------
LETTERS = "กขคง"
WEBQ = {}
KEY = []  # (หัวข้อ, [(เลขข้อ, ตัวอักษร, อธิบาย)])

def build_quiz(items, start=1, offset=0):
    out, key = [], []
    for i, (q, ch, ex) in enumerate(items):
        correct = ch[0]
        order = list(range(4))
        random.shuffle(order)
        pos = order.index(0)
        opts = "".join(
            f'<div class="opt"><span class="lt">{LETTERS[k]}</span><span>{fmt(ch[j])}</span></div>'
            for k, j in enumerate(order))
        n = start + i
        out.append(f'<div class="q"><div class="qn">{n}</div><div class="qb"><p class="qt">{fmt(q)}</p>{opts}</div></div>')
        key.append((n, LETTERS[pos], ex))
        WEBQ.setdefault(id(items), []).append((n, q, [ch[j] for j in order], pos, ex))
    return "".join(out), key

def key_table(key):
    rows = "".join(f'<tr><td class="kn">{n}</td><td class="ka">{a}</td><td>{fmt(e)}</td></tr>' for n, a, e in key)
    return f'<table class="keytbl"><tr><th>ข้อ</th><th>ตอบ</th><th>เหตุผลสั้น ๆ</th></tr>{rows}</table>'

q1, k1 = build_quiz(P1)
q2, k2 = build_quiz(P2)
q3, k3 = build_quiz(P3)
qf, kf = build_quiz(FINAL)
qx, kx = build_quiz(PX)
q2f, k2f = build_quiz(F2)
q3f, k3f = build_quiz(F3)
for _z in (Z1, Z2, Z3, Z4, Z5):
    build_quiz(_z)

cheat = "".join(f'<div class="ch"><b>{a}</b><span>{b}</span></div>' for a, b in CHEAT)

CSS = """
@page { size: A4; margin: 14mm 13mm 16mm 13mm; }
:root{
  --pri:#0b5cab; --pri2:#1e88e5; --ink:#12263a; --mut:#5a6b7d; --line:#d6e3f1;
  --soft:#eef5fc; --soft2:#f6f9fd; --ok:#0f7b5f; --warn:#b4540a; --code:#0f2b46;
}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact; print-color-adjust:exact}
body{margin:0; font-family:'Sarabun','Leelawadee UI','Tahoma',sans-serif; font-size:10.6pt; line-height:1.55; color:var(--ink); background:#fff}
code,pre{font-family:'JetBrains Mono','Consolas','Courier New',monospace}
code{background:var(--soft); color:var(--pri); padding:0 4px; border-radius:4px; font-size:.86em; border:1px solid var(--line)}
h1,h2,h3,h4{margin:0}
.cover{height:262mm; display:flex; flex-direction:column; justify-content:center; padding:0 6mm; page-break-after:always;
  background:linear-gradient(160deg,#fff 55%,var(--soft) 100%)}
.cover .tag{display:inline-block; align-self:flex-start; background:var(--pri); color:#fff; padding:3px 12px; border-radius:20px; font-size:10pt; font-weight:600; letter-spacing:.3px}
.cover h1{font-size:40pt; line-height:1.15; margin:14px 0 8px; color:var(--pri); font-weight:800}
.cover .sub{font-size:15pt; color:var(--mut); margin-bottom:26px}
.cover .meta{display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:10px 0 24px}
.cover .meta div{border:1.5px solid var(--line); background:#fff; border-radius:12px; padding:12px 14px}
.cover .meta b{display:block; font-size:12pt; color:var(--pri)}
.cover .meta span{font-size:9.6pt; color:var(--mut)}
.toc{border-left:4px solid var(--pri2); padding:4px 0 4px 14px; font-size:11pt}
.toc div{margin:3px 0}
.part{page-break-before:always}
.phead{display:flex; align-items:center; gap:14px; background:var(--pri); color:#fff; border-radius:14px; padding:12px 18px; margin-bottom:12px}
.phead .no{font-size:26pt; font-weight:800; opacity:.95; line-height:1}
.phead h2{font-size:17pt; font-weight:700; line-height:1.2}
.phead small{display:block; font-size:9.6pt; opacity:.88; font-weight:400}
h3{font-size:13pt; color:var(--pri); margin:14px 0 6px; padding-bottom:3px; border-bottom:2px solid var(--line); page-break-after:avoid}
h4{font-size:10.8pt; color:var(--pri); margin-bottom:3px}
ul,ol{margin:4px 0 6px; padding-left:20px} li{margin:2px 0}
p{margin:4px 0}
.grid2{display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:8px 0}
.card{border:1.5px solid var(--line); background:var(--soft2); border-radius:10px; padding:8px 12px; page-break-inside:avoid}
.card ul,.card ol{margin:2px 0; padding-left:18px}
.note{background:var(--soft); border-left:4px solid var(--pri2); border-radius:6px; padding:7px 12px; margin:8px 0; page-break-inside:avoid}
.tip{background:#fff8e8; border-left:4px solid #e8a317; border-radius:6px; padding:6px 12px; margin:8px 0; font-size:10pt; page-break-inside:avoid}
.good{background:#eaf7f2; border:1.5px solid #9fd8c4; border-radius:10px; padding:8px 12px; color:#0a5a45}
.bad{background:#fdeeea; border:1.5px solid #f0b4a3; border-radius:10px; padding:8px 12px; color:#8a2d12}
pre{background:var(--code); color:#e6f0fa; border-radius:10px; padding:10px 13px; font-size:8.6pt; line-height:1.5; margin:8px 0; white-space:pre-wrap; word-break:break-word; page-break-inside:avoid}
pre .c{color:#8fb3d9}
.grid2 pre{margin:0}
table{border-collapse:collapse; width:100%; margin:8px 0; font-size:9.8pt; page-break-inside:avoid}
th{background:var(--pri); color:#fff; text-align:left; padding:5px 9px; font-weight:600}
td{padding:5px 9px; border-bottom:1px solid var(--line); vertical-align:top}
tr:nth-child(even) td{background:var(--soft2)}
.cheat{display:grid; grid-template-columns:1fr 1fr; gap:6px 10px; margin-top:6px}
.ch{border:1.5px solid var(--line); border-radius:8px; padding:5px 10px; display:flex; flex-direction:column; background:#fff; font-size:9.6pt; page-break-inside:avoid}
.ch b{color:var(--pri)}
.quizhead{background:var(--soft); border:1.5px solid var(--pri2); border-radius:12px; padding:9px 16px; margin:0 0 10px; display:flex; justify-content:space-between; align-items:center}
.quizhead h2{font-size:15pt; color:var(--pri)} .quizhead span{color:var(--mut); font-size:10pt}
.q{display:flex; gap:10px; margin:0 0 11px; page-break-inside:avoid}
.qn{flex:0 0 28px; height:28px; border-radius:50%; background:var(--pri); color:#fff; font-weight:700; display:flex; align-items:center; justify-content:center; font-size:10.5pt}
.qb{flex:1}
.qt{font-weight:600; margin:2px 0 4px}
.opt{display:flex; gap:8px; margin:2px 0; padding:3px 8px; border:1px solid var(--line); border-radius:7px}
.lt{flex:0 0 18px; color:var(--pri); font-weight:700}
.key{page-break-before:always}
.keytbl td.kn{width:34px; font-weight:700; color:var(--pri); text-align:center}
.keytbl td.ka{width:42px; font-weight:800; color:var(--ok); text-align:center}
.keytbl{font-size:9.4pt; page-break-inside:auto}
.keytbl tr{page-break-inside:avoid}
.ksec{margin-top:12px; font-size:12.5pt; color:var(--pri); font-weight:700; page-break-after:avoid}
.score{margin-top:10px; border:1.5px dashed var(--pri2); border-radius:10px; padding:8px 14px; color:var(--mut)}
"""

def quiz_page(title, sub, qhtml, cls="part"):
    return f'<section class="{cls}"><div class="quizhead"><h2>{title}</h2><span>{sub}</span></div>{qhtml}</section>'

def part(no, title, sub, body, extra=""):
    return (f'<section class="part"><div class="phead"><div class="no">{no}</div>'
            f'<div><h2>{title}</h2><small>{sub}</small></div></div>{body}{extra}</section>')

doc = f"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<title>ITDS241 Node.js สรุป + ข้อสอบ</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>

<section class="cover">
 <span class="tag">ITDS241 · Web Technologies and Application</span>
 <h1>Node.js<br>สรุปสอบ + ฝึกข้อสอบ</h1>
 <div class="sub">Lecture 09–11 · Part I · II · III</div>
 <div class="meta">
  <div><b>3 พาร์ท</b><span>สรุปอ่านจบพาร์ทละ ~5 นาที รวม ~15 นาที</span></div>
  <div><b>30 + 30 ข้อ</b><span>ข้อสอบพาร์ทละ 10 ข้อ และข้อสอบรวม 30 ข้อ</span></div>
  <div><b>มีเฉลย</b><span>เฉลยพร้อมเหตุผลท้ายเล่ม</span></div>
 </div>
 <div class="toc">
  <div><b>Part 1</b> Intro to Node.js, Module, fs, http server</div>
  <div><b>Part 2</b> Express, Routing, Static files, Form (GET/POST)</div>
  <div><b>Part 3</b> .env, Cookie, Session, MySQL</div>
  <div><b>ข้อสอบรวม</b> 30 ข้อ ครอบคลุมทุกหัวข้อ</div>
 </div>
</section>

{part("1","Intro to Node.js","Lecture 09 · Node.js Part I", S1)}
{quiz_page("ข้อสอบ Part 1","10 ข้อ · พื้นฐาน Node.js / Module / fs / http", q1)}
{part("2","Express Framework","Lecture 10 · Node.js Part II", S2)}
{quiz_page("ข้อสอบ Part 2","10 ข้อ · Express / Routing / Static / Form", q2)}
{part("3","Cookie, Session, Database","Lecture 11 · Node.js Part III", S3)}
{quiz_page("ข้อสอบ Part 3","10 ข้อ · .env / Cookie / Session / MySQL", q3)}

<section class="part">
 <div class="phead"><div class="no">★</div><div><h2>สรุปด่วนก่อนเข้าห้องสอบ</h2><small>อ่านหน้านี้หน้าเดียวก็จำหัวใจได้</small></div></div>
 <div class="cheat">{cheat}</div>
 <div class="tip" style="margin-top:12px"><b>ข้อที่มักพลาด:</b> (1) Node ไม่มี <code>window</code>/<code>document</code> · (2) <code>readFileSync</code> = blocking · (3) route 404 ต้องอยู่ท้ายสุด · (4) POST ต้องมี <code>express.urlencoded</code> · (5) Cookie อยู่ client / Session อยู่ server · (6) <code>maxAge</code> หน่วยเป็นมิลลิวินาที · (7) ต้อง <code>dotenv.config()</code> ก่อนใช้ <code>process.env</code></div>
</section>

{quiz_page("ข้อสอบรวม 30 ข้อ","ครอบคลุม Lecture 09–11 · ระดับพื้นฐาน · เลือกคำตอบที่ถูกที่สุด", qf)}

<section class="key">
 <div class="phead"><div class="no">✓</div><div><h2>เฉลย</h2><small>ตรวจคำตอบพร้อมเหตุผล</small></div></div>
 <div class="ksec">Part 1</div>{key_table(k1)}
 <div class="ksec">Part 2</div>{key_table(k2)}
 <div class="ksec">Part 3</div>{key_table(k3)}
 <div class="ksec">ข้อสอบรวม 30 ข้อ</div>{key_table(kf)}
 <div class="score">เกณฑ์ประเมินตัวเอง: 27–30 พร้อมสอบ · 21–26 ทบทวนหัวข้อที่พลาด · ต่ำกว่า 21 อ่านสรุปอีกรอบ</div>
</section>
</body></html>"""

out_html = os.path.join(HERE, "_print.html")
out_pdf = os.path.join(HERE, "ITDS241-NodeJS-Summary-Quiz.pdf")
open(out_html, "w", encoding="utf-8").write(doc)
print("html ok")


# ================= เวอร์ชันเว็บ (HTML อ่านบนจอ + ทำข้อสอบโต้ตอบ) =================
WCSS = """
:root{--bg:#f4f8fd;--card:#fff;--ink:#12263a;--mut:#5a6b7d;--line:#d6e3f1;--pri:#0b5cab;--pri2:#1e88e5;--soft:#eef5fc;--soft2:#f6f9fd;--code:#0f2b46;--codeink:#e6f0fa;--okbg:#e3f6ee;--ok:#0f7b5f;--badbg:#fdeeea;--bad:#b3341a;--tipbg:#fff8e8}
:root[data-theme=dark]{--bg:#0c1824;--card:#13243a;--ink:#e4edf7;--mut:#94a8be;--line:#25405e;--pri:#6db3f2;--pri2:#4aa3ee;--soft:#16304c;--soft2:#112239;--code:#08121d;--codeink:#dcebfa;--okbg:#10382d;--ok:#5fd4aa;--badbg:#3b1d17;--bad:#ff9c85;--tipbg:#3a2f12}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0c1824;--card:#13243a;--ink:#e4edf7;--mut:#94a8be;--line:#25405e;--pri:#6db3f2;--pri2:#4aa3ee;--soft:#16304c;--soft2:#112239;--code:#08121d;--codeink:#dcebfa;--okbg:#10382d;--ok:#5fd4aa;--badbg:#3b1d17;--bad:#ff9c85;--tipbg:#3a2f12}}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:70px}
body{margin:0;background:var(--bg);color:var(--ink);font:1rem/1.6 'Sarabun','Leelawadee UI',Tahoma,sans-serif}
code,pre{font-family:'JetBrains Mono',Consolas,monospace}
code{background:var(--soft);color:var(--pri);padding:1px 6px;border-radius:5px;font-size:.85em;border:1px solid var(--line)}
nav{position:sticky;top:0;z-index:9;background:var(--card);border-bottom:1px solid var(--line);display:flex;gap:6px;align-items:center;padding:8px 16px;overflow-x:auto}
nav a{color:var(--ink);text-decoration:none;padding:6px 12px;border-radius:20px;font-size:15px;white-space:nowrap;min-height:36px;display:flex;align-items:center}
nav a:hover{background:var(--soft)}nav .sp{flex:1}
button.tg{border:1px solid var(--line);background:var(--soft);color:var(--ink);border-radius:20px;padding:6px 14px;font:inherit;font-size:15px;cursor:pointer;min-height:36px;white-space:nowrap}
main{max-width:1680px;margin:0 auto;padding:12px 32px 64px}
main>section:not(#quiz),.hero{max-width:880px;margin-left:auto;margin-right:auto}
.hero{padding:36px 0 12px}.hero .tag{display:inline-block;background:var(--pri);color:var(--bg);padding:3px 14px;border-radius:20px;font-size:14px;font-weight:600}
.hero h1{font-weight:600;font-size:clamp(28px,5vw,42px);line-height:1.15;margin:14px 0 6px;color:var(--pri)}.hero p{color:var(--mut);margin:0}
section{margin-top:32px}
.ph{display:flex;gap:14px;align-items:center;background:var(--pri);color:var(--bg);border-radius:16px;padding:14px 20px}
.ph .no{font-size:28px;font-weight:600;line-height:1}.ph h2{margin:0;font-size:20px;font-weight:600}.ph small{opacity:.85;font-size:14px}
h3{font-weight:600;color:var(--pri);font-size:18px;margin:28px 0 8px;padding-bottom:4px;border-bottom:2px solid var(--line)}h4{margin:0 0 4px;color:var(--pri)}
ul,ol{padding-left:22px}li{margin:3px 0}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 16px}
.note{background:var(--soft);border-left:4px solid var(--pri2);border-radius:8px;padding:10px 16px;margin:12px 0}
.tip{background:var(--tipbg);border-left:4px solid #e8a317;border-radius:8px;padding:8px 16px;margin:12px 0;font-size:15.5px}
.good{background:var(--okbg);color:var(--ok);border-radius:12px;padding:10px 16px}.bad{background:var(--badbg);color:var(--bad);border-radius:12px;padding:10px 16px}
pre{background:var(--code);color:var(--codeink);border-radius:12px;padding:14px 16px;font-size:14px;line-height:1.55;overflow-x:auto;margin:12px 0}pre .c{color:#7fa6d1}
.grid2 pre{margin:0}
.tw{overflow-x:auto;margin:12px 0}table{border-collapse:collapse;width:100%;font-size:15.5px;background:var(--card)}
th{background:var(--pri);color:var(--bg);text-align:left;padding:8px 12px}td{padding:8px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.cheat{display:grid;grid-template-columns:1fr 1fr;gap:10px}.ch{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 14px;display:flex;flex-direction:column;font-size:15.5px}.ch b{color:var(--pri)}
.qz{margin-top:14px;display:grid;gap:16px}
.q{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.qt{font-weight:600;margin:0 0 8px}.qt .n{display:inline-flex;width:30px;height:30px;border-radius:50%;background:var(--pri);color:var(--bg);align-items:center;justify-content:center;font-size:15px;margin-right:8px}
.o{display:flex;gap:10px;width:100%;text-align:left;font:inherit;font-size:16px;color:var(--ink);background:var(--soft2);border:1.5px solid var(--line);border-radius:10px;padding:9px 12px;margin:6px 0;cursor:pointer;min-height:44px;align-items:flex-start}
.o:hover{border-color:var(--pri2)}.o .lt{font-weight:700;color:var(--pri);flex:0 0 18px}
.o.right{background:var(--okbg);border-color:var(--ok)}.o.wrong{background:var(--badbg);border-color:var(--bad)}
.q.done .o{cursor:default}
.ex{display:none;margin-top:8px;padding:8px 12px;background:var(--soft);border-radius:8px;font-size:15px}.q.done .ex{display:block}
.bar{display:flex;justify-content:space-between;align-items:center;margin-top:12px;font-weight:600;color:var(--pri)}
.bar button{border:1px solid var(--line);background:var(--soft);color:var(--ink);border-radius:10px;padding:6px 14px;font:inherit;cursor:pointer;min-height:40px}
@media(max-width:640px){.grid2,.cheat{grid-template-columns:1fr}body{font-size:16px}}
:focus-visible{outline:3px solid var(--pri2);outline-offset:2px}
"""

def wquiz(sid, items):
    rows = []
    for n, q, opts, pos, ex in WEBQ[id(items)]:
        o = "".join(f'<button class="o" data-i="{k}"><span class="lt">{LETTERS[k]}</span><span>{fmt(t)}</span></button>' for k, t in enumerate(opts))
        rows.append(f'<div class="q" data-a="{pos}"><p class="qt"><span class="n">{n}</span>{fmt(q)}</p>{o}<div class="ex"><b>เฉลย {LETTERS[pos]}</b> — {fmt(ex)}</div></div>')
    return (f'<div class="qz" id="{sid}-qz">{"".join(rows)}</div>'
            f'<div class="bar"><span>คะแนน <span id="{sid}-sc">0</span> / {len(rows)}</span><button data-reset="{sid}">ทำใหม่</button></div>')

def tw(s):
    return s.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")


# ---------- ข้อสอบแบบแอป (ชุด / ตารางเลขข้อ / ถูก-ผิด) ----------
import json as _json

def _items(items):
    return [{"q": q, "o": o, "a": a, "e": e} for n, q, o, a, e in WEBQ[id(items)]]

SETS = {
    "x": {"name": "ซ้อมสอบ 1", "lec": ["ซ้อมสอบ · Basic 10 ข้อ"], "cut": [10], "items": _items(PX)},
    "p1": {"name": "Part 1", "lec": ["Lecture 9 · Node.js"], "cut": [10], "items": _items(P1)},
    "p2": {"name": "Part 2", "lec": ["Lecture 10 · Express"], "cut": [10], "items": _items(P2)},
    "p3": {"name": "Part 3", "lec": ["Lecture 11 · Cookie/Session/DB"], "cut": [10], "items": _items(P3)},
    "f": {"name": "ข้อสอบรวม 1", "lec": ["Lecture 9 · Node.js", "Lecture 10 · Express", "Lecture 11 · Cookie/Session/DB"],
          "cut": [10, 20, 30], "items": _items(FINAL)},
    "f2": {"name": "ข้อสอบรวม 2", "lec": ["Lecture 9 · Node.js", "Lecture 10 · Express", "Lecture 11 · Cookie/Session/DB"], "cut": [10, 20, 30], "items": _items(F2)},
    "f3": {"name": "ข้อสอบรวม 3", "lec": ["Lecture 9 · Node.js", "Lecture 10 · Express", "Lecture 11 · Cookie/Session/DB"], "cut": [10, 20, 30], "items": _items(F3)},
    "z1": {"name": "ซ้อมสอบ 2", "lec": ["Lecture 9 · Node.js", "Lecture 10 · Express", "Lecture 11 · Cookie/Session/DB"], "cut": [7, 14, 20], "items": _items(Z1)},
    "z2": {"name": "ซ้อมสอบ 3", "lec": ["Lecture 9 · Node.js", "Lecture 10 · Express", "Lecture 11 · Cookie/Session/DB"], "cut": [7, 14, 20], "items": _items(Z2)},
    "z3": {"name": "ซ้อมสอบ 4", "lec": ["Lecture 9 · Node.js", "Lecture 10 · Express", "Lecture 11 · Cookie/Session/DB"], "cut": [7, 14, 20], "items": _items(Z3)},
    "z4": {"name": "ซ้อมสอบ 5", "lec": ["Lecture 9 · Node.js", "Lecture 10 · Express", "Lecture 11 · Cookie/Session/DB"], "cut": [7, 14, 20], "items": _items(Z4)},
    "z5": {"name": "ซ้อมสอบ 6", "lec": ["Lecture 9 · Node.js", "Lecture 10 · Express", "Lecture 11 · Cookie/Session/DB"], "cut": [7, 14, 20], "items": _items(Z5)},
}

QCSS = """
.nav .btn,nav .tgl{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:5px 11px;font:inherit;font-size:15px;cursor:pointer;min-height:36px}
.qapp{display:grid;grid-template-columns:260px minmax(0,1fr);gap:24px;margin-top:16px;align-items:start}
.lbl{font-size:14px;color:var(--mut);margin:14px 0 6px;font-weight:600}.lbl:first-child{margin-top:0}
.sets{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sets button{font-weight:500;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:10px;padding:8px 6px;font:inherit;font-weight:500;font-size:14px;cursor:pointer;min-height:38px}
.sets button.on{background:#14213d;color:#fff;border-color:#14213d;box-shadow:0 0 0 2px var(--bg),0 0 0 4px #0f7b5f}
:root[data-theme=dark] .sets button.on{background:#e4edf7;color:#0c1824;border-color:#e4edf7}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}
.stats div{background:var(--card);border:1px solid var(--line);border-radius:10px;text-align:center;padding:8px 2px}
.stats b{display:block;font-weight:600;font-size:22px;line-height:1.1}.stats span{font-size:13px;color:var(--mut)}
#sc-ok{color:#0f7b5f}#sc-bad{color:#c0304b}#sc-no{color:var(--ink)}
:root[data-theme=dark] #sc-ok{color:#5fd4aa}:root[data-theme=dark] #sc-bad{color:#ff8fa3}
.ngrid{display:grid;grid-template-columns:repeat(6,1fr);gap:7px}
.ngrid button{padding:0;min-width:0;aspect-ratio:1;min-height:34px;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:6px;font:inherit;font-size:13px;font-weight:500;cursor:pointer}
.ngrid button.ok{background:#e3f6ee;border-color:#0f7b5f;color:#0a5a45}.ngrid button.bad{background:#fdeaee;border-color:#c0304b;color:#9b1e38}
:root[data-theme=dark] .ngrid button.ok{background:#10382d;color:#8fe6c4}:root[data-theme=dark] .ngrid button.bad{background:#3b1d24;color:#ffb3c0}
.ngrid button.cur{outline:3px solid var(--pri2);outline-offset:1px}
.legend{display:flex;gap:12px;font-size:13px;color:var(--mut);margin:8px 0 12px}.legend i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:4px;vertical-align:-1px;border:1.5px solid var(--line)}
.legend .a{background:#0f7b5f;border-color:#0f7b5f}.legend .b{background:#c0304b;border-color:#c0304b}
.qside .act{font-size:14px;display:block;width:100%;text-align:left;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:10px;padding:8px 12px;margin-top:6px;font:inherit;font-size:14px;cursor:pointer;min-height:38px}
.qc{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px 28px;margin-bottom:16px}
.qh{display:flex;justify-content:space-between;gap:10px;align-items:center;color:var(--mut);font-size:15px;flex-wrap:wrap}
.tag{background:#e3f6ee;color:#0a5a45;border-radius:6px;padding:3px 10px;font-size:13px;font-weight:600}
:root[data-theme=dark] .tag{background:#10382d;color:#8fe6c4}
.qc h3{border:0;margin:14px 0 14px;font-size:1.1rem;font-weight:500;line-height:1.5;color:var(--ink);padding:0}
.opt{font-size:15px;display:flex;gap:12px;align-items:center;width:100%;text-align:left;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:10px;padding:8px 14px;margin:7px 0;font:inherit;font-size:15px;cursor:pointer;min-height:44px}
.opt:hover:not(:disabled){border-color:var(--pri2)}
.opt .lt{flex:0 0 26px;height:26px;border-radius:6px;background:var(--soft);display:grid;place-items:center;font-weight:600;font-size:13px;color:var(--mut)}
.opt.right{background:#e3f6ee;border-color:#0f7b5f}.opt.right .lt{background:#0f7b5f;color:#fff}
.opt.wrong{background:#fdeaee;border-color:#c0304b}.opt.wrong .lt{background:#c0304b;color:#fff}
:root[data-theme=dark] .opt.right{background:#10382d}:root[data-theme=dark] .opt.wrong{background:#3b1d24}
.opt.dim{opacity:.55}.opt:disabled{cursor:default}
.fb{font-size:14.5px;background:var(--soft);border-radius:10px;padding:10px 16px;margin-top:12px}.fb b{display:block;margin-bottom:2px}
.fb.ok b{color:#0f7b5f}.fb.no b{color:#c0304b}:root[data-theme=dark] .fb.ok b{color:#5fd4aa}:root[data-theme=dark] .fb.no b{color:#ff8fa3}
.qn2{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:20px}
.qn2 button{border:1px solid var(--line);font-size:14px;background:var(--card);color:var(--ink);border-radius:8px;padding:8px 18px;font:inherit;font-weight:500;cursor:pointer;min-height:40px}
.qn2 .nx{background:#14213d;color:#fff;border-color:#14213d}:root[data-theme=dark] .qn2 .nx{background:#e4edf7;color:#0c1824}
.qn2 button:disabled{opacity:.4;cursor:default}.qn2 small{color:var(--mut);text-align:center}
.brk{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-top:14px}
.brk div{border:1px solid var(--line);border-radius:10px;padding:10px 14px}.brk b{font-size:24px;display:block}.brk span{font-size:13px;color:var(--mut)}
.goq{display:inline-block;margin-top:8px;padding:8px 16px;border-radius:10px;background:var(--pri);color:var(--bg);text-decoration:none;font-weight:600}
.opt.right{color:#0a3d2f}.opt.wrong{color:#6b1226}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--x:0}
:root:not([data-theme=light]) .opt.right{background:#10382d;color:#d9fff0}:root:not([data-theme=light]) .opt.wrong{background:#3b1d24;color:#ffd9e0}
:root:not([data-theme=light]) .ngrid button.ok{background:#10382d;color:#8fe6c4}:root:not([data-theme=light]) .ngrid button.bad{background:#3b1d24;color:#ffb3c0}
:root:not([data-theme=light]) .fb.ok b,:root:not([data-theme=light]) #sc-ok{color:#5fd4aa}:root:not([data-theme=light]) .fb.no b,:root:not([data-theme=light]) #sc-bad{color:#ff8fa3}
:root:not([data-theme=light]) .tag{background:#10382d;color:#8fe6c4}:root:not([data-theme=light]) .sets button.on{background:#e4edf7;color:#0c1824;border-color:#e4edf7}:root:not([data-theme=light]) .qn2 .nx{background:#e4edf7;color:#0c1824}}
:root[data-theme=dark] .opt.right{color:#d9fff0}:root[data-theme=dark] .opt.wrong{color:#ffd9e0}
@media(max-width:820px){.qapp{grid-template-columns:1fr}.qc{padding:18px 16px}.qn2 small{display:none}}
"""

QJS = """
(function(){
var SETS=__SETS__;
var r=document.documentElement;
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
var th=ls('th');if(th)r.setAttribute('data-theme',th);
document.getElementById('tg').onclick=function(){var d=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');var n=d==='dark'?'light':'dark';r.setAttribute('data-theme',n);ls('th',n)};
var fs=+ls('fs')||15;function setFs(){r.style.fontSize=fs+'px';ls('fs',fs)}setFs();
document.getElementById('fm').onclick=function(){fs=Math.max(14,fs-1);setFs()};
document.getElementById('fp').onclick=function(){fs=Math.min(24,fs+1);setFs()};
var L='กขคง';
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/`([^`]+)`/g,'<code>$1</code>')}
var ans={};try{ans=JSON.parse(ls('qans')||'{}')}catch(e){}
var cur={},set='x';
function A(s){if(!ans[s]||ans[s].length!==SETS[s].items.length)ans[s]=SETS[s].items.map(function(){return null});return ans[s]}
function save(){ls('qans',JSON.stringify(ans))}
function lecOf(s,i){var c=SETS[s].cut,k=0;while(k<c.length-1&&i>=c[k])k++;return SETS[s].lec[k]}
function $(id){return document.getElementById(id)}
function render(){
 var S=SETS[set],a=A(set),n=S.items.length,i=cur[set]||0,it=S.items[i];
 [].forEach.call($('sets').children,function(b){b.classList.toggle('on',b.dataset.s===set)});
 var ok=0,bad=0;a.forEach(function(v,k){if(v!==null){if(v===S.items[k].a)ok++;else bad++}});
 $('sc-ok').textContent=ok;$('sc-bad').textContent=bad;$('sc-no').textContent=n-ok-bad;$('gl').textContent='ข้อสอบ '+n+' ข้อ';
 $('ngrid').innerHTML=S.items.map(function(_,k){var v=a[k],c=v===null?'':(v===S.items[k].a?'ok':'bad');return '<button class="'+c+(k===i?' cur':'')+'" data-k="'+k+'" aria-label="ข้อ '+(k+1)+'">'+(k+1)+'</button>'}).join('');
 var h='<div class="qh"><span>'+S.name+' · ข้อ '+(i+1)+' จาก '+n+'</span><span class="tag">'+lecOf(set,i)+'</span></div><h3>'+esc(it.q)+'</h3>';
 var done=a[i]!==null;
 h+=it.o.map(function(t,k){var c='opt';if(done){if(k===it.a)c+=' right';else if(k===a[i])c+=' wrong';else c+=' dim'}
  return '<button class="'+c+'" data-o="'+k+'"'+(done?' disabled':'')+'><span class="lt">'+L[k]+'</span><span>'+esc(t)+'</span></button>'}).join('');
 if(done){var good=a[i]===it.a;h+='<div class="fb '+(good?'ok':'no')+'"><b>'+(good?'ถูกต้อง':'ไม่ถูกต้อง — คำตอบที่ถูกคือข้อ '+L[it.a])+'</b>'+esc(it.e)+'</div>'}
 h+='<div class="qn2"><button id="pv"'+(i===0?' disabled':'')+'>ข้อก่อนหน้า</button><small>กด 1–4 เพื่อตอบ, ← → เพื่อเปลี่ยนข้อ</small><button class="nx" id="nx"'+(i===n-1?' disabled':'')+'>ข้อถัดไป</button></div>';
 $('qc').innerHTML=h;
 $('pv').onclick=function(){go(i-1)};$('nx').onclick=function(){go(i+1)};
 [].forEach.call($('qc').querySelectorAll('.opt'),function(b){b.onclick=function(){pick(+b.dataset.o)}});
 [].forEach.call($('ngrid').children,function(b){b.onclick=function(){go(+b.dataset.k)}});
 var all=ok+bad===n;$('sum').hidden=!all;
 if(all){var pc=Math.round(ok/n*100),br=[],cut=S.cut,st=0;
  cut.forEach(function(e,k){var g=0;for(var j=st;j<e;j++)if(a[j]===S.items[j].a)g++;br.push('<div><b>'+g+' / '+(e-st)+'</b><span>'+S.lec[k]+'</span></div>');st=e});
  $('sum').innerHTML='<h3 style="margin-top:0">ทำครบแล้ว ได้ '+ok+' / '+n+' ('+pc+'%)</h3><p>'+(pc>=90?'พร้อมสอบแล้ว ลองชุดถัดไปได้เลย':pc>=70?'ใกล้แล้ว ลองทำเฉพาะข้อที่ผิดใหม่':'ทบทวนเนื้อหาอีกรอบ แล้วกลับมาทำใหม่')+'</p><div class="brk">'+br.join('')+'</div>'}
}
function go(k){var n=SETS[set].items.length;cur[set]=Math.max(0,Math.min(n-1,k));render()}
function pick(o){var a=A(set);if(a[cur[set]||0]!==null)return;a[cur[set]||0]=o;save();render()}
$('sets').onclick=function(e){var b=e.target.closest('button');if(b){set=b.dataset.s;render()}};
$('redo-all').onclick=function(){ans[set]=null;A(set);cur[set]=0;save();render()};
$('redo-wrong').onclick=function(){var a=A(set),S=SETS[set],f=-1;a.forEach(function(v,k){if(v!==null&&v!==S.items[k].a){a[k]=null;if(f<0)f=k}});if(f>=0)cur[set]=f;save();render()};
document.addEventListener('keydown',function(e){if(/input|textarea|select/i.test(e.target.tagName))return;
 if(e.key>='1'&&e.key<='4')pick(+e.key-1);else if(e.key==='ArrowRight')go((cur[set]||0)+1);else if(e.key==='ArrowLeft')go((cur[set]||0)-1)});
$('sets').innerHTML=Object.keys(SETS).map(function(s){return '<button data-s="'+s+'">'+SETS[s].name+'</button>'}).join('');
render();
})();
"""

TIP = ('<div class="tip"><b>ข้อที่มักพลาด:</b> (1) Node ไม่มี <code>window</code>/<code>document</code> · (2) <code>readFileSync</code> = blocking · '
       '(3) route 404 ต้องอยู่ท้ายสุด · (4) POST ต้องมี <code>express.urlencoded</code> · (5) Cookie อยู่ client / Session อยู่ server · '
       '(6) <code>maxAge</code> หน่วยเป็นมิลลิวินาที · (7) ต้อง <code>dotenv.config()</code> ก่อนใช้ <code>process.env</code></div>')

def wsec(sid, no, title, small, body):
    return (f'<section id="{sid}"><div class="ph"><div class="no">{no}</div><div><h2>{title}</h2><small>{small}</small></div></div>'
            f'{tw(body)}<a class="goq" href="#quiz" data-set="{sid}">ทำข้อสอบ {title} →</a></section>')

web = ('<!doctype html><html lang="th"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1">'
 '<title>Node.js สรุปสอบ ITDS241</title>'
 '<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">'
 f'<style>{WCSS}{QCSS}</style></head><body>'
 '<nav><a href="#p1">Part 1</a><a href="#p2">Part 2</a><a href="#p3">Part 3</a><a href="#cheat">สรุปด่วน</a><a href="#quiz"><b>ข้อสอบ</b></a><span class="sp"></span>'
 '<button class="tgl" id="fm" aria-label="ลดขนาดตัวอักษร">ก−</button><button class="tgl" id="fp" aria-label="เพิ่มขนาดตัวอักษร">ก+</button>'
 '<button class="tg" id="tg" aria-label="สลับธีมสว่าง/มืด">☀/🌙 ธีม</button></nav><main>'
 '<div class="hero"><span class="tag">ITDS241 · Web Technologies and Application</span><h1>Node.js สรุปสอบ + ฝึกข้อสอบ</h1>'
 '<p>Lecture 09–11 · สรุป ~15 นาที · ซ้อมสอบ 6 ชุด + ข้อสอบ 10 ข้อ/พาร์ท + ข้อสอบรวม 3 ชุด · ดูผลถูก-ผิดรายข้อได้</p></div>'
 + wsec("p1", "1", "Intro to Node.js", "Lecture 09 · Part I", S1)
 + wsec("p2", "2", "Express Framework", "Lecture 10 · Part II", S2)
 + wsec("p3", "3", "Cookie, Session, Database", "Lecture 11 · Part III", S3)
 + f'<section id="cheat"><div class="ph"><div class="no">★</div><div><h2>สรุปด่วนก่อนเข้าห้องสอบ</h2></div></div><div class="cheat" style="margin-top:14px">{cheat}</div>{TIP}</section>'
 + '<section id="quiz"><div class="ph"><div class="no">✎</div><div><h2>ข้อสอบ</h2><small>เลือกชุด · กดเลือกคำตอบ · ดูข้อที่ถูก/ผิดในตารางซ้าย</small></div></div>'
 '<div class="qapp"><aside class="qside"><div class="lbl">เลือกชุด</div><div class="sets" id="sets"></div>'
 '<div class="stats"><div><b id="sc-ok">0</b><span>ถูก</span></div><div><b id="sc-bad">0</b><span>ผิด</span></div><div><b id="sc-no">0</b><span>ยังไม่ทำ</span></div></div>'
 '<div class="lbl" id="gl"></div><div class="ngrid" id="ngrid"></div>'
 '<div class="legend"><span><i class="a"></i>ถูก</span><span><i class="b"></i>ผิด</span><span><i></i>ยังไม่ทำ</span></div>'
 '<button class="act" id="redo-wrong">ทำเฉพาะข้อที่ผิดใหม่</button><button class="act" id="redo-all">เริ่มชุดนี้ใหม่ทั้งหมด</button></aside>'
 '<div class="qmain"><div class="qc" id="qc"></div><div class="qc" id="sum" hidden></div></div></div></section>'
 '</main><script>' + QJS.replace("__SETS__", _json.dumps(SETS, ensure_ascii=False))
 + '''
document.querySelectorAll('.goq').forEach(function(a){a.addEventListener('click',function(){var b=document.querySelector('#sets [data-s="'+a.dataset.set+'"]');if(b)b.click()})});
</script></body></html>''')
open(os.path.join(HERE, "ITDS241-NodeJS-Summary-Quiz.html"), "w", encoding="utf-8").write(web)
print("web ok")
