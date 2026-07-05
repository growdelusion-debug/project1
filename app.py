import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(page_title="헤르조르센", layout="centered")

# 세션 상태 초기화 (게임 단계 관리: 'START', 'FACTION_SELECT', 'GAME_PLAY')
if 'stage' not in st.session_state:
    st.session_state.stage = 'START'
if 'faction' not in st.session_state:
    st.session_state.faction = None

# --- 1. 첫 화면 (사극 풍, 붉은 느낌) ---
if st.session_state.stage == 'START':
    st.markdown("""
        <style>
        .stApp {
            background-color: #3a0000;
            color: #f1e4c3;
        }
        .main-title {
            font-family: 'Gungsuh', '궁서체', serif;
            font-size: 60px;
            font-weight: bold;
            color: #d11a2a;
            text-align: center;
            text-shadow: 2px 2px 4px #000000;
            margin-top: 50px;
        }
        .desc-text {
            font-size: 20px;
            text-align: center;
            margin-top: 30px;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-title">헤르조르센</div>', unsafe_allow_html=True)
    st.markdown('<div class="desc-text">당신은 헤르조르센에 떨어진 효령대군입니다.<br>각 스테이지마다 자신의 파를 선택 후 승리하십시오!</div>', unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # 중앙 정렬 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("게임 시작하기", use_container_width=True):
            st.session_state.stage = 'FACTION_SELECT'
            st.rerun()

# --- 2. 진영 선택 화면 ---
elif st.session_state.stage == 'FACTION_SELECT':
    st.markdown("""
        <style>
        .stApp { background-color: #1a1a1a; color: white; }
        .select-title { text-align: center; font-size: 32px; margin-bottom: 30px; }
        .faction-box { border: 2px solid #444; padding: 20px; border-radius: 10px; text-align: center; background-color: #2a2a2a; }
        .char-img { font-size: 70px; margin-bottom: 10px; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="select-title">진영을 선택하십시오</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="faction-box">', unsafe_allow_html=True)
        st.markdown('<div class="char-img">🙋‍♂️🐈</div>', unsafe_allow_html=True) # 고양이를 들고 있는 사람 대용 이모지
        st.markdown('<h3>캣맘파</h3>', unsafe_allow_html=True)
        st.markdown('<p>적: 희생당한 새들의 원혼<br>무기: 새총 (돌멩이)</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("캣맘파 선택", use_container_width=True):
            st.session_state.faction = 'catmom'
            
    with col2:
        st.markdown('<div class="faction-box">', unsafe_allow_html=True)
        st.markdown('<div class="char-img">🩹🕊️</div>', unsafe_allow_html=True) # 부상당한 새 대용 이모지
        st.markdown('<h3>캣싫어파</h3>', unsafe_allow_html=True)
        st.markdown('<p>적: 고양이를 안은 사람들<br>무기: 물총 (물줄기)</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("캣싫어파 선택", use_container_width=True):
            st.session_state.faction = 'catloathe'

    st.write("---")
    if st.session_state.faction:
        selected_name = "캣맘파" if st.session_state.faction == 'catmom' else "캣싫어파"
        st.success(f"현재 선택된 진영: **{selected_name}**")
        
        if st.button("선택 완료, 전쟁 시작", use_container_width=True):
            st.session_state.stage = 'GAME_PLAY'
            st.rerun()

# --- 3. 게임 플레이 화면 (HTML5 Canvas + JS) ---
elif st.session_state.stage == 'GAME_PLAY':
    st.markdown("<style>.stApp { background-color: #121212; }</style>", unsafe_allow_html=True)
    
    # JavaScript 연동용 진영 데이터 변수
    faction_type = st.session_state.faction
    
    # 웹 게임 시스템 구현 (HTML/JS)
    game_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ margin: 0; padding: 0; background-color: #121212; color: white; font-family: sans-serif; text-align: center; overflow: hidden; }}
            #gameContainer {{ position: relative; width: 500px; margin: 10px auto; }}
            canvas {{ background: linear-gradient(to bottom, #757575, #bdc3c7); border: 4px solid #333; border-radius: 5px; display: block; }}
            #overlay {{ position: absolute; top: 0; left: 0; width: 500px; height: 600px; pointer-events: none; box-sizing: border-box; transition: background 0.1s; }}
            .danger-glow {{ animation: blink 0.5s infinite alternate; }}
            @keyframes blink {{ from {{ box-shadow: inset 0 0 0px red; }} to {{ box-shadow: inset 0 0 50px red; }} }}
            #countdownOverlay {{ position: absolute; top: 0; left: 0; width: 500px; height: 600px; background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center; font-size: 80px; font-weight: bold; color: #fff; }}
            #resultScreen {{ position: absolute; top: 0; left: 0; width: 500px; height: 600px; background: black; display: none; flex-direction: column; justify-content: center; align-items: center; }}
            .win-text {{ color: #FFD700; font-size: 60px; font-weight: bold; font-family: serif; }}
            .lose-text {{ color: #808080; font-size: 60px; font-weight: bold; font-family: serif; }}
            .score-info {{ font-size: 20px; margin: 20px; color: white; }}
            .restart-btn {{ padding: 10px 30px; font-size: 18px; background-color: #444; color: white; border: none; border-radius: 5px; cursor: pointer; }}
            .restart-btn:hover {{ background-color: #666; }}
        </style>
    </head>
    <body>

    <div id="gameContainer">
        <canvas id="gameCanvas" width="500" height="600"></canvas>
        <div id="overlay"></div>
        <div id="countdownOverlay">3</div>
        
        <div id="resultScreen">
            <div id="resultStatus"></div>
            <div id="resultScores" class="score-info"></div>
            <button class="restart-btn" onclick="restartGame()">다시하기</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const overlay = document.getElementById('overlay');
        const countdownOverlay = document.getElementById('countdownOverlay');
        const resultScreen = document.getElementById('resultScreen');

        // 게임 설정 변수
        const faction = "{faction_type}"; // 'catmom' 또는 'catloathe'
        let gameActive = false;
        let startCountdown = 3;
        let timeLeft = 120; // 2분 (120초)
        
        let playerLines = [62, 187, 312, 437]; // 4개의 무기 거점 X 좌표
        let playerY = 540;
        
        let myScore = 0;
        let enemyScore = 0;

        let enemies = [];
        let projectiles = [];
        let enemySpawnTimer = 0;

        // 적 캐릭터 및 투사체 설정
        // 캣맘파 선택 -> 적: 부상당한 새(🕊️), 내 무기: 새총(🪨)
        // 캣싫어파 선택 -> 적: 고양이 든 사람(🙋‍♂️), 내 무기: 물총(💧)
        const enemyEmoji = faction === 'catmom' ? '🕊️' : '🙋‍♂️';
        const weaponEmoji = faction === 'catmom' ? '🎯' : '🔫'; // 무기 본체 이모지
        const bulletEmoji = faction === 'catmom' ? '🪨' : '💧';

        // 3초 카운트다운 시작
        let countInterval = setInterval(() => {{
            startCountdown--;
            if (startCountdown > 0) {{
                countdownOverlay.innerText = startCountdown;
            }} else if (startCountdown === 0) {{
                countdownOverlay.innerText = "START!";
            }} else {{
                clearInterval(countInterval);
                countdownOverlay.style.display = 'none';
                gameActive = true;
                gameLoop();
                startTimer();
            }}
        }}, 1000);

        // 2분 타이머 구동
        function startTimer() {{
            let timerInterval = setInterval(() => {{
                if (!gameActive) {{
                    clearInterval(timerInterval);
                    return;
                }}
                timeLeft--;

                // 10초 이하일 때 빨간 불빛 깜빡임 작동
                if (timeLeft <= 10) {{
                    overlay.classList.add('danger-glow');
                }}

                if (timeLeft <= 0) {{
                    clearInterval(timerInterval);
                    endGame();
                }}
            }}, 1000);
        }}

        // 키보드/마우스 입력 처리 (1,2,3,4 키를 누르거나 무기 클릭 시 발사)
        window.addEventListener('keydown', (e) => {{
            if (!gameActive) return;
            if (e.key === '1') shoot(0);
            if (e.key === '2') shoot(1);
            if (e.key === '3') shoot(2);
            if (e.key === '4') shoot(3);
        }});

        canvas.addEventListener('mousedown', (e) => {{
            if (!gameActive) return;
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            
            // 방어 구역(아래쪽 클릭 시 해당 라인에서 발사)
            if (mouseY > 450) {{
                if (mouseX < 125) shoot(0);
                else if (mouseX < 250) shoot(1);
                else if (mouseX < 375) shoot(2);
                else shoot(3);
            }}
        }});

        function shoot(lineIndex) {{
            projectiles.push({{
                x: playerLines[lineIndex] + 12,
                y: playerY - 20,
                speed: 7
            }});
        }}

        // 적 생성 시스템
        function spawnEnemy() {{
            const randomLine = Math.floor(Math.random() * 4);
            enemies.push({{
                x: playerLines[randomLine] + 5,
                y: -30,
                speed: 2 + Math.random() * 2,
                line: randomLine
            }});
        }}

        // 메인 게임 루프
        function gameLoop() {{
            if (!gameActive) return;

            // 배경 그리기 (현대식 회색 아스팔트/콘크리트 느낌 구역 분할)
            ctx.fillStyle = "#bdc3c7"; 
            ctx.fillRect(0, 0, 500, 600);

            // 구역 구분선 그리기 (공격 구역 상단 / 방어 구역 하단 450px 기준)
            ctx.strokeStyle = "#7f8c8d";
            ctx.lineWidth = 2;
            for(let i=1; i<4; i++) {{
                ctx.beginPath();
                ctx.moveTo(i * 125, 0);
                ctx.lineTo(i * 125, 600);
                ctx.stroke();
            }}

            // 방어 구역 구분 가로선
            ctx.strokeStyle = "#34495e";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(0, 480);
            ctx.lineTo(500, 480);
            ctx.stroke();
            
            // 방어 구역 배경색 살짝 다르게
            ctx.fillStyle = "rgba(52, 73, 94, 0.2)";
            ctx.fillRect(0, 480, 500, 120);

            // 타이머 & 점수 텍스트 상단 출력
            ctx.fillStyle = "#000000";
            ctx.font = "bold 18px sans-serif";
            ctx.fillText("남은 시간: " + timeLeft + "초", 20, 30);
            ctx.fillText("우리 팀 점수: " + myScore, 350, 30);
            ctx.fillText("상대 팀 점수: " + enemyScore, 350, 55);

            // 무기 본체(4개 거점) 그리기
            ctx.font = "30px sans-serif";
            for (let i = 0; i < 4; i++) {{
                ctx.fillText(weaponEmoji, playerLines[i], playerY);
                // 안내 숫자키 고지
                ctx.font = "12px sans-serif";
                ctx.fillStyle = "#333";
                ctx.fillText("[" + (i+1) + "]", playerLines[i]+10, playerY+25);
                ctx.font = "30px sans-serif";
            }}

            // 적 스폰 조절
            enemySpawnTimer++;
            if (enemySpawnTimer > 40) {{ 
                spawnEnemy();
                enemySpawnTimer = 0;
            }}

            // 투사체 이동 및 렌더링
            for (let i = projectiles.length - 1; i >= 0; i--) {{
                let p = projectiles[i];
                p.y -= p.speed;
                ctx.font = "20px sans-serif";
                ctx.fillText(bulletEmoji, p.x, p.y);

                // 화면 밖으로 나가면 제거
                if (p.y < 0) {{
                    projectiles.splice(i, 1);
                }}
            }}

            // 적 이동, 렌더링 및 충돌체크
            for (let i = enemies.length - 1; i >= 0; i--) {{
                let e = enemies[i];
                e.y += e.speed;
                ctx.font = "35px sans-serif";
                ctx.fillText(enemyEmoji, e.x, e.y);

                // 방어 구역 침투 검사 (Y선 480px 침투 시)
                if (e.y > 480) {{
                    enemyScore += 10; // 상대 팀 방어구역 침투 시 10점 획득
                    enemies.splice(i, 1);
                    continue;
                }}

                // 내 투사체와 적의 충돌 검사
                for (let j = projectiles.length - 1; j >= 0; j--) {{
                    let p = projectiles[j];
                    // 거리 기준 충돌 계산
                    if (Math.abs(p.x - (e.x + 15)) < 25 && Math.abs(p.y - e.y) < 30) {{
                        myScore += 5; // 우리 팀이 상대 맞출 시 5점 획득
                        enemies.splice(i, 1);
                        projectiles.splice(j, 1);
                        break;
                    }}
                }}
            }}

            requestAnimationFrame(gameLoop);
        }}

        // 게임 종료 처리
        function endGame() {{
            gameActive = false;
            overlay.classList.remove('danger-glow');
            
            const statusDiv = document.getElementById('resultStatus');
            const scoresDiv = document.getElementById('resultScores');
            
            if (myScore > enemyScore) {{
                statusDiv.innerHTML = '<div class="win-text">WIN</div>';
            }} else {{
                statusDiv.innerHTML = '<div class="lose-text">LOSE</div>';
            }}

            scoresDiv.innerHTML = "우리 팀: " + myScore + "점 vs 상대 팀: " + enemyScore + "점";
            resultScreen.style.display = 'flex';
        }}

        // 다시하기 버튼 기능 (부모 Streamlit 창을 리로드하여 초기화)
        function restartGame() {{
            window.parent.location.reload();
        }}
    </script>
    </body>
    </html>
    """
    
    # 세로 높이에 맞춘 컴포넌트 삽입
    components.html(game_html, height=620)
