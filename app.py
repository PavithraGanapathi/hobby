"""
VAISE - General Intelligence & Reasoning Assessment
Clean, modern, responsive quiz application with dark aesthetic,
glowing cyan buttons, question grid tracker, custom Chocolate Shower reward,
and dynamic Web Audio sound effects ("Hooray!" for correct, "Ohh!" for incorrect).
"""

import streamlit as st
import streamlit.components.v1 as components
import random

# ==============================================================================
# 1. PAGE CONFIGURATION & RESPONSIVE SETUP
# ==============================================================================
st.set_page_config(
    page_title="VAISE | Intelligence & Reasoning Assessment",
    page_icon="🍫",
    layout="centered",
    initial_sidebar_state="auto"  # Automatically collapses on mobile screens
)

# Custom High-End Styling: Dark Cockpit Theme + Glowing Cyan Buttons + High-Contrast Options
st.markdown("""
<style>
    /* Base Global Theme */
    .stApp {
        background-color: #070d18 !important;
        color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Responsive Mobile Guard */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 1.5rem !important;
            max-width: 100% !important;
        }
        .header-card {
            padding: 16px 14px !important;
        }
        .header-title {
            font-size: 1.5rem !important;
        }
        .question-box {
            padding: 18px 16px !important;
        }
        .question-text {
            font-size: 1.15rem !important;
        }
    }

    /* VAISE Main Header */
    .header-card {
        background: linear-gradient(135deg, #0d1a2d 0%, #08111e 100%);
        border: 2px solid #0284c7;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 0 25px rgba(2, 132, 199, 0.25), inset 0 0 15px rgba(6, 182, 212, 0.1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .header-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #06b6d4, #10b981, #f59e0b, #06b6d4);
        background-size: 200% 100%;
        animation: headerScan 3s linear infinite;
    }
    .header-badge {
        display: inline-block;
        background: rgba(6, 182, 212, 0.15);
        color: #22d3ee !important;
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 2px;
        padding: 4px 14px;
        border-radius: 999px;
        border: 1px solid rgba(6, 182, 212, 0.4);
        margin-bottom: 8px;
        text-transform: uppercase;
        font-family: monospace;
    }
    .header-title {
        color: #ffffff !important;
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: 1px;
        margin: 4px 0 6px 0;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    }
    .header-subtitle {
        color: #94a3b8 !important;
        font-size: 1rem;
        font-weight: 500;
        margin: 0;
    }

    /* Live HUD Bar */
    .hud-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 10px 18px;
        margin-bottom: 16px;
        font-family: monospace;
        font-size: 0.92rem;
    }
    .hud-stat {
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 700;
    }
    .streak-fire {
        color: #f59e0b;
        animation: flamePulse 1s infinite alternate;
    }

    /* Question Container Box */
    .question-box {
        background: #0d1a2d !important;
        border: 1.5px solid rgba(56, 189, 248, 0.35);
        border-radius: 14px;
        padding: 24px 26px;
        margin-bottom: 18px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    }
    .category-tag {
        display: inline-block;
        background: rgba(14, 165, 233, 0.15) !important;
        color: #38bdf8 !important;
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        padding: 5px 12px;
        border-radius: 6px;
        margin-bottom: 14px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        font-family: monospace;
    }
    .question-text {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        line-height: 1.6;
        color: #f8fafc !important;
        margin-bottom: 16px;
    }

    /* Tactical Expander for Formulas & Hints */
    div[data-testid="stExpander"] {
        background: rgba(13, 26, 45, 0.6) !important;
        border: 1.5px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
        margin: 12px 0 16px 0 !important;
    }
    div[data-testid="stExpander"] summary {
        color: #38bdf8 !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        padding: 8px 12px !important;
    }
    div[data-testid="stExpander"] summary:hover {
        color: #22d3ee !important;
    }
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
        padding: 0 12px 10px 12px !important;
    }

    /* Visual Box for ASCII & Tables */

    .visual-container {
        background: #050b14 !important;
        border: 2px dashed #0284c7 !important;
        border-radius: 8px;
        padding: 14px;
        margin: 14px 0 18px 0;
        font-family: "JetBrains Mono", "Courier New", monospace;
        font-size: 1rem;
        font-weight: 700;
        color: #34d399 !important;
        text-align: center;
        overflow-x: auto;
        white-space: pre-wrap;
    }

    /* ========================================================= */
    /* ULTRA HIGH-CONTRAST ILLUMINATED OPTION CARDS             */
    /* Crisp white background with bold pitch-black text        */
    /* ========================================================= */
    div[data-testid="stRadio"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 22px !important;
    }

    /* Radio Group Title */
    div[data-testid="stRadio"] > label {
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 12px !important;
        display: block !important;
        font-family: monospace;
    }

    /* Stack of Options */
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
    }

    /* Each Option Card */
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: #ffffff !important;
        border: 2.5px solid #38bdf8 !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3), 0 0 12px rgba(56, 189, 248, 0.15) !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Hover effect */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: #f0fdf4 !important;
        border-color: #10b981 !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4), 0 0 15px rgba(16, 185, 129, 0.3) !important;
        transform: translateY(-2px) scale(1.01) !important;
    }

    /* Pitch-Black Text inside options for WCAG AAA Readability */
    div[data-testid="stRadio"] div[role="radiogroup"] > label p,
    div[data-testid="stRadio"] div[role="radiogroup"] > label span,
    div[data-testid="stRadio"] div[role="radiogroup"] > label div {
        color: #020617 !important;
        font-size: 1.12rem !important;
        font-weight: 800 !important;
        opacity: 1 !important;
        letter-spacing: -0.2px !important;
    }

    /* Active / Checked State */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background-color: #e0f2fe !important;
        border-color: #0284c7 !important;
        border-width: 3px !important;
        box-shadow: 0 0 20px rgba(2, 132, 199, 0.6) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
        color: #0369a1 !important;
    }

    /* ========================================================= */
    /* GLOWING ACTION BUTTONS (CYAN ACCENT & PULSE)              */
    /* ========================================================= */
    .stButton > button {
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-size: 1.15rem !important;
        font-weight: 900 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important;
        border: 2px solid #38bdf8 !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.5), 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        animation: tacticalPulse 2s infinite ease-in-out !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #22d3ee 0%, #0ea5e9 100%) !important;
        box-shadow: 0 0 35px rgba(34, 211, 238, 0.8), 0 0 50px rgba(14, 165, 233, 0.4) !important;
        transform: translateY(-2px) scale(1.02) !important;
    }
    @keyframes tacticalPulse {
        0%, 100% {
            box-shadow: 0 0 16px rgba(6, 182, 212, 0.45), 0 4px 12px rgba(0, 0, 0, 0.4);
        }
        50% {
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.85), 0 0 45px rgba(6, 182, 212, 0.3);
        }
    }

    /* Feedback Cards */
    .feedback-correct {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(5, 150, 105, 0.28) 100%) !important;
        border: 2.5px solid #10b981 !important;
        border-radius: 12px !important;
        padding: 20px 22px !important;
        margin: 20px 0 !important;
        color: #a7f3d0 !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.3) !important;
        animation: fadeIn 0.3s ease-in-out;
    }
    .feedback-incorrect {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.18) 0%, rgba(220, 38, 38, 0.28) 100%) !important;
        border: 2.5px solid #ef4444 !important;
        border-radius: 12px !important;
        padding: 20px 22px !important;
        margin: 20px 0 !important;
        color: #fecaca !important;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.3) !important;
        animation: fadeIn 0.3s ease-in-out;
    }
    .feedback-phrase {
        font-size: 1.35rem !important;
        font-weight: 900 !important;
        margin-bottom: 8px !important;
    }
    .feedback-detail {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        margin-bottom: 6px !important;
    }
    .feedback-explanation {
        font-size: 0.98rem !important;
        line-height: 1.6 !important;
        margin-top: 12px !important;
        padding-top: 12px !important;
        border-top: 1.5px dashed rgba(255, 255, 255, 0.2) !important;
        color: #f8fafc !important;
    }

    /* ========================================================= */
    /* UNIFORM 5x4 QUESTION TRACKER GRID IN SIDEBAR              */
    /* ========================================================= */
    .waypoint-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 6px;
        margin: 12px 0 18px 0;
    }
    .wp-box {
        aspect-ratio: 1 / 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
        font-weight: 800;
        font-family: monospace;
        border-radius: 6px;
        transition: all 0.2s ease;
        user-select: none;
    }
    .wp-correct {
        background: rgba(16, 185, 129, 0.2) !important;
        color: #34d399 !important;
        border: 1.5px solid #10b981 !important;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.35);
    }
    .wp-wrong {
        background: rgba(239, 68, 68, 0.2) !important;
        color: #f87171 !important;
        border: 1.5px solid #ef4444 !important;
        box-shadow: 0 0 8px rgba(239, 68, 68, 0.25);
    }
    .wp-current {
        background: linear-gradient(135deg, #0284c7 0%, #06b6d4 100%) !important;
        color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        box-shadow: 0 0 14px rgba(6, 182, 212, 0.75) !important;
        animation: wpPulse 1.4s infinite alternate;
    }
    .wp-pending {
        background: rgba(30, 41, 59, 0.7) !important;
        color: #64748b !important;
        border: 1px solid rgba(71, 85, 105, 0.5) !important;
    }
    @keyframes wpPulse {
        0% { transform: scale(1); box-shadow: 0 0 6px rgba(6, 182, 212, 0.4); }
        100% { transform: scale(1.08); box-shadow: 0 0 16px rgba(6, 182, 212, 0.9); }
    }

    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #0b1424 !important;
        border-right: 1.5px solid #1e293b !important;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9;
    }

    /* ========================================================= */
    /* CUSTOM FULL-SCREEN CHOCOLATE SHOWER ANIMATION             */
    /* ========================================================= */
    .chocolate-shower-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 999999;
        overflow: hidden;
    }
    .falling-treat {
        position: absolute;
        top: -70px;
        animation-name: treatFall;
        animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94);
        animation-fill-mode: forwards;
        user-select: none;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.4));
    }
    @keyframes treatFall {
        0% {
            transform: translateY(0) rotate(0deg) scale(0.7);
            opacity: 1;
        }
        85% {
            opacity: 1;
        }
        100% {
            transform: translateY(105vh) rotate(420deg) scale(1.15);
            opacity: 0;
        }
    }

    /* Summary Card */
    .summary-card {
        background: linear-gradient(135deg, #0a192f 0%, #172554 100%) !important;
        border: 3px solid #f59e0b !important;
        border-radius: 16px !important;
        padding: 34px 24px !important;
        text-align: center !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7), 0 0 25px rgba(245, 158, 11, 0.25) !important;
        color: #ffffff !important;
        margin-bottom: 24px !important;
    }
    .stat-pill {
        background: #0d1a2d !important;
        border: 1.5px solid #1e3a8a !important;
        border-radius: 12px !important;
        padding: 16px 10px !important;
        text-align: center !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.4) !important;
    }
    .stat-num {
        font-size: 2.1rem !important;
        font-weight: 900 !important;
        color: #38bdf8 !important;
        font-family: monospace;
    }
    .stat-label {
        font-size: 0.8rem !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        font-weight: 700 !important;
    }

    /* Animations */
    @keyframes headerScan {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    @keyframes flamePulse {
        0% { transform: scale(1); filter: drop-shadow(0 0 2px #f59e0b); }
        100% { transform: scale(1.15); filter: drop-shadow(0 0 8px #f59e0b); }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. AUDIO SYNTHESIZER ("Hooray!" for Correct, "Ohh!" for Incorrect)
# ==============================================================================
def play_sound_effect(is_correct: bool):
    """
    Plays native audio sound effects using the Web Audio API and SpeechSynthesis:
    - If correct: Upbeat victory fanfare chord + cheerful 'Hooray!' voice.
    - If incorrect: Comical descending wah-wah slide + sympathetic 'Ohh!' voice.
    """
    if is_correct:
        sound_js = """
        <script>
        (function() {
            try {
                // 1. Web Audio API Fanfare Chime
                const AudioCtx = window.AudioContext || window.webkitAudioContext || (window.parent && (window.parent.AudioContext || window.parent.webkitAudioContext));
                if (AudioCtx) {
                    const ctx = new AudioCtx();
                    const now = ctx.currentTime;
                    // Major victory arpeggio: C5 (523Hz), E5 (659Hz), G5 (784Hz), C6 (1046Hz)
                    const notes = [
                        { f: 523.25, t: 0.0, d: 0.32, v: 0.28 },
                        { f: 659.25, t: 0.08, d: 0.32, v: 0.28 },
                        { f: 783.99, t: 0.16, d: 0.40, v: 0.32 },
                        { f: 1046.50, t: 0.25, d: 0.65, v: 0.38 }
                    ];
                    notes.forEach(n => {
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.type = 'triangle';
                        osc.frequency.setValueAtTime(n.f, now + n.t);
                        gain.gain.setValueAtTime(0.001, now + n.t);
                        gain.gain.linearRampToValueAtTime(n.v, now + n.t + 0.02);
                        gain.gain.exponentialRampToValueAtTime(0.0001, now + n.t + n.d);
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start(now + n.t);
                        osc.stop(now + n.t + n.d);
                    });
                }
                // 2. Celebratory 'Hooray!' Voice
                const synth = window.speechSynthesis || (window.parent && window.parent.speechSynthesis);
                if (synth) {
                    synth.cancel();
                    const utter = new SpeechSynthesisUtterance("Hooray!");
                    utter.rate = 1.15;
                    utter.pitch = 1.45;
                    utter.volume = 1.0;
                    synth.speak(utter);
                }
            } catch(e) {
                console.log("Audio play error", e);
            }
        })();
        </script>
        """
    else:
        sound_js = """
        <script>
        (function() {
            try {
                // 1. Web Audio API Descending Wah-Wah Slide
                const AudioCtx = window.AudioContext || window.webkitAudioContext || (window.parent && (window.parent.AudioContext || window.parent.webkitAudioContext));
                if (AudioCtx) {
                    const ctx = new AudioCtx();
                    const now = ctx.currentTime;
                    // Descending sliding tones
                    const slides = [
                        { f1: 360, f2: 310, t: 0.0, d: 0.22, v: 0.25 },
                        { f1: 310, f2: 260, t: 0.18, d: 0.25, v: 0.25 },
                        { f1: 260, f2: 190, t: 0.38, d: 0.50, v: 0.30 }
                    ];
                    slides.forEach(s => {
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(s.f1, now + s.t);
                        osc.frequency.linearRampToValueAtTime(s.f2, now + s.t + s.d);
                        
                        gain.gain.setValueAtTime(0.001, now + s.t);
                        gain.gain.linearRampToValueAtTime(s.v, now + s.t + 0.03);
                        gain.gain.exponentialRampToValueAtTime(0.0001, now + s.t + s.d);
                        
                        const filter = ctx.createBiquadFilter();
                        filter.type = 'lowpass';
                        filter.frequency.setValueAtTime(750, now + s.t);
                        
                        osc.connect(filter);
                        filter.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start(now + s.t);
                        osc.stop(now + s.t + s.d);
                    });
                }
                // 2. Sympathetic 'Ohh!' Voice
                const synth = window.speechSynthesis || (window.parent && window.parent.speechSynthesis);
                if (synth) {
                    synth.cancel();
                    const utter = new SpeechSynthesisUtterance("Ohh!");
                    utter.rate = 0.85;
                    utter.pitch = 0.70;
                    utter.volume = 0.95;
                    synth.speak(utter);
                }
            } catch(e) {
                console.log("Audio play error", e);
            }
        })();
        </script>
        """
    components.html(sound_js, height=0, width=0)


# ==============================================================================
# 3. CHOCOLATE SHOWER REWARD FUNCTION
# ==============================================================================
def trigger_chocolate_shower():
    """Renders a full-screen cascade of falling chocolate and candy emojis."""
    emojis = ["🍫", "🍬", "🍩", "🍪", "🍭", "🧁"]
    items = []
    # Generate 45 randomly scattered falling treats
    for i in range(45):
        emoji = random.choice(emojis)
        left_pos = random.randint(1, 98)
        delay = round(random.uniform(0.0, 1.8), 2)
        duration = round(random.uniform(2.2, 3.8), 2)
        font_size = round(random.uniform(1.6, 2.7), 2)
        items.append(
            f'<span class="falling-treat" style="left:{left_pos}%; animation-delay:{delay}s; animation-duration:{duration}s; font-size:{font_size}rem;">{emoji}</span>'
        )
    
    shower_html = f"""
    <div class="chocolate-shower-container">
        {''.join(items)}
    </div>
    """
    st.markdown(shower_html, unsafe_allow_html=True)


# ==============================================================================
# 4. ENTHUSIASTIC & RESILIENT FEEDBACK POOLS
# ==============================================================================
CORRECT_FEEDBACK_POOL = [
    "🍫🎯 Spot on! Excellent answer!",
    "🍬🔥 Outstanding! You nailed that deduction!",
    "🍩🌟 Absolute perfection! Brilliant thinking!",
    "🍪💡 Sharp logic! Full marks on this question!",
    "🍫🧠 Fantastic analytical reasoning!",
    "🍬✨ Clean, crisp, and accurate! Keep this up!",
    "🍩🎉 Bingo! That's 100% correct!",
    "🍪🚀 Brilliant work! Right on the mark!",
    "🍫👏 Great job! Your deduction is flawless!",
    "🍬💯 Perfect answer! Moving strong!",
    "🍩⚡ Super fast and completely accurate!",
    "🍪🏆 Top-tier deduction! Great intelligence work!",
    "🍫⭐ Brilliant clarity! You saw right through that pattern!",
    "🍬🎯 Bullseye! Flawless solution!",
    "🍩🙌 Excellent deduction! You're cruising smoothly!"
]

INCORRECT_FEEDBACK_POOL = [
    "💪 Don't worry, you'll get the next one! Shake it off and focus!",
    "🚀 A minor setback! Review the explanation below and keep moving!",
    "🌪️ Almost had it! Keep pushing, maintain your composure!",
    "💡 Good attempt! Check the reasoning below and press forward!",
    "📈 Mistakes are part of learning! Onward to the next question!",
    "🥊 Shake it out! Focus on the next challenge ahead!",
    "⚡ Don't lose focus! The next question is yours to conquer!",
    "🛡️ Review the concept above and nail the upcoming question!",
    "🌱 Every attempt makes you sharper! Reset and continue!",
    "🎯 Very close! Check the solution details below and advance!",
    "🧭 Take a breath, absorb the logic, and keep your head in the game!",
    "✨ You have this! Focus 100% on the next problem!"
]


# ==============================================================================
# 5. QUESTION BANK (Exactly 20 Medium-Difficulty Questions)
# ==============================================================================
def get_mixed_oir_bank():
    """Returns exactly 20 medium-difficulty reasoning questions (Comprehensive Mixed Set)."""
    return [
        {
            "id": 1,
            "category": "Verbal Reasoning (Analogy)",
            "question": "Complete the analogy: \n\n**RADAR : RADIO WAVES :: SONAR : ?**",
            "visual": None,
            "options": [
                "A) Light Rays",
                "B) Sound Waves",
                "C) Magnetic Flux",
                "D) Infrared Radiation"
            ],
            "answer": "B) Sound Waves",
            "explanation": "RADAR uses radio waves to detect objects in the air, while SONAR uses acoustic/sound waves to detect objects underwater."
        },
        {
            "id": 2,
            "category": "Series Completion (Numbers)",
            "question": "Find the missing number in the sequence: \n\n**3,  8,  18,  38,  78,  ?**",
            "visual": None,
            "options": [
                "A) 148",
                "B) 156",
                "C) 158",
                "D) 162"
            ],
            "answer": "C) 158",
            "explanation": "Pattern 1: The difference doubles each time: +5, +10, +20, +40, +80. Thus, 78 + 80 = 158.\nPattern 2: (Previous Number × 2) + 2: (78 × 2) + 2 = 156 + 2 = 158."
        },
        {
            "id": 3,
            "category": "Coding & Decoding",
            "question": "In a code language, if **COLD** is coded as **FROH**, how will **FLEET** be encoded under the same rule?",
            "visual": None,
            "options": [
                "A) HOFFW",
                "B) IOHHW",
                "C) JNIIX",
                "D) INGGV"
            ],
            "answer": "B) IOHHW",
            "explanation": "Each letter is shifted forward by +3 alphabetical positions:\n• C(+3)=F, O(+3)=R, L(+3)=O, D(+3)=H.\nApplying +3 to FLEET:\n• F(+3)=I, L(+3)=O, E(+3)=H, E(+3)=H, T(+3)=W → **IOHHW**."
        },
        {
            "id": 4,
            "category": "Direction & Angle Reasoning",
            "question": "A traveler begins facing **090° (Due East)**. They make a turn of **135° clockwise**, followed by a turn of **180° counter-clockwise**. What is their final heading and direction?",
            "visual": "Initial Heading: 090° (East)  -->  +135° (CW)  -->  -180° (CCW)",
            "options": [
                "A) 045° (North-East)",
                "B) 135° (South-East)",
                "C) 225° (South-West)",
                "D) 315° (North-West)"
            ],
            "answer": "A) 045° (North-East)",
            "explanation": "Net heading adjustment = (+135° CW) - (180° CCW) = -45° (i.e. 45° counter-clockwise).\nInitial Heading 090° - 45° = 045°, which points North-East."
        },
        {
            "id": 5,
            "category": "Spatial Reasoning (Unfolded Cube Net)",
            "question": "A standard die is unfolded into the following net layout. When reassembled into a 3D cube, which numbered face will be **directly opposite to Face 3**?",
            "visual": """
      +---+
      | 1 |
  +---+---+---+
  | 2 | 3 | 4 |
  +---+---+---+
      | 5 |
      +---+
      | 6 |
      +---+""",
            "options": [
                "A) Face 1",
                "B) Face 2",
                "C) Face 5",
                "D) Face 6"
            ],
            "answer": "D) Face 6",
            "explanation": "In an unfolded cube net, alternate faces along a straight line fold into opposite pairs:\n• Face 2 is opposite Face 4\n• Face 1 is opposite Face 5\n• Therefore, Face 3 is directly opposite Face 6."
        },
        {
            "id": 6,
            "category": "Classification (Odd One Out)",
            "question": "Identify the odd one out among the following instruments:",
            "visual": None,
            "options": [
                "A) Magnetic Compass",
                "B) Marine Sextant",
                "C) Chronometer",
                "D) Submarine Periscope"
            ],
            "answer": "D) Submarine Periscope",
            "explanation": "Compass, Sextant, and Chronometer are primary instruments for navigation and location tracking. A Periscope is an optical viewing device for submerged observation."
        },
        {
            "id": 7,
            "category": "Alphanumeric Series Completion",
            "question": "Identify the logical term that replaces the question mark: \n\n**A2Z,  C4X,  E8V,  G16T,  ?**",
            "visual": None,
            "options": [
                "A) H32S",
                "B) I32R",
                "C) I24R",
                "D) J32Q"
            ],
            "answer": "B) I32R",
            "explanation": "• First letter advances by +2: A, C, E, G, **I**\n• Middle number doubles: 2, 4, 8, 16, **32**\n• Third letter steps back by -2: Z, X, V, T, **R**\nCombining all three gives **I32R**."
        },
        {
            "id": 8,
            "category": "Spatial Aptitude (Painted Cube Cuts)",
            "question": "A solid wooden cube of side 4 cm is painted blue on all six faces. It is subsequently cut into uniform smaller 1 cm cubes (total 64 small cubes). How many small cubes will have **EXACTLY TWO** painted faces?",
            "visual": "Formula for n x n x n cube: Edges (excluding corners) = 12 × (n - 2)",
            "options": [
                "A) 16",
                "B) 24",
                "C) 32",
                "D) 8"
            ],
            "answer": "B) 24",
            "explanation": "Cubes with exactly 2 painted faces lie along the 12 edges (excluding the 8 corner cubes).\nFormula = 12 × (n - 2). Here n = 4.\nNumber of cubes = 12 × (4 - 2) = 12 × 2 = **24**."
        },
        {
            "id": 9,
            "category": "Speed, Time & Distance",
            "question": "A high-speed train travels at a constant cruising speed of **360 km/h**. If it travels for **25 minutes**, what distance has it covered?",
            "visual": None,
            "options": [
                "A) 120 km",
                "B) 150 km",
                "C) 175 km",
                "D) 180 km"
            ],
            "answer": "B) 150 km",
            "explanation": "Distance = Speed × Time.\nTime in hours = 25 / 60 hours.\nDistance = 360 km/h × (25 / 60) = 6 × 25 = **150 km**."
        },
        {
            "id": 10,
            "category": "Logical Deduction (Syllogism)",
            "question": "Evaluate the statements and conclusions:\n\n**Statements:**\n1. All managers are leaders.\n2. No leader is reckless.\n3. Some consultants are managers.\n\n**Conclusions:**\nI. Some consultants are leaders.\nII. No manager is reckless.",
            "visual": None,
            "options": [
                "A) Only Conclusion I follows",
                "B) Only Conclusion II follows",
                "C) Both Conclusions I and II follow",
                "D) Neither Conclusion I nor II follows"
            ],
            "answer": "C) Both Conclusions I and II follow",
            "explanation": "• Since some consultants are managers and all managers are leaders, those consultants are leaders (Conclusion I follows).\n• Since all managers are leaders and no leader is reckless, no manager can be reckless (Conclusion II follows)."
        },
        {
            "id": 11,
            "category": "Clock Angle Logic",
            "question": "At **04:40** on an analog clock, what is the exact acute angle between the hour hand and the minute hand?",
            "visual": "Angle Formula: | 30 × H - 5.5 × M |",
            "options": [
                "A) 90°",
                "B) 100°",
                "C) 110°",
                "D) 120°"
            ],
            "answer": "B) 100°",
            "explanation": "Using the standard clock angle formula: |30 × H - (11/2) × M|\nFor H = 4 and M = 40:\n|30 × 4 - 5.5 × 40| = |120 - 220| = |-100| = **100°**."
        },
        {
            "id": 12,
            "category": "Matrix Pattern Reasoning",
            "question": "Determine the missing value in the third row of the matrix below:",
            "visual": """
+--------+--------+--------+
|   7    |   9    |   32   |
+--------+--------+--------+
|   6    |   8    |   28   |
+--------+--------+--------+
|   5    |   7    |   ?    |
+--------+--------+--------+""",
            "options": [
                "A) 20",
                "B) 22",
                "C) 24",
                "D) 26"
            ],
            "answer": "C) 24",
            "explanation": "Pattern: In each row, the 3rd number equals the difference of squares of the first two numbers:\n• Row 1: 9² - 7² = 81 - 49 = 32 (also (7+9)×2 = 32)\n• Row 2: 8² - 6² = 64 - 36 = 28 (also (6+8)×2 = 28)\n• Row 3: 7² - 5² = 49 - 25 = **24** (also (5+7)×2 = 24)."
        },
        {
            "id": 13,
            "category": "Coding & Decoding (Letter Sum)",
            "question": "In a cipher system, if **GAME** is coded as **26** and **PLAY** is coded as **54**, what is the encoded value for **WING**?",
            "visual": None,
            "options": [
                "A) 49",
                "B) 51",
                "C) 53",
                "D) 57"
            ],
            "answer": "C) 53",
            "explanation": "The code is the direct sum of alphabetical positions:\n• GAME: G(7) + A(1) + M(13) + E(5) = 26\n• PLAY: P(16) + L(12) + A(1) + Y(25) = 54\n• WING: W(23) + I(9) + N(14) + G(7) = **53**."
        },
        {
            "id": 14,
            "category": "Spatial Reflection & Symmetry",
            "question": "How many individual letters in the word **NAVAL** remain completely identical to themselves when reflected in a vertical mirror?",
            "visual": "Word: N  A  V  A  L   |   [Vertical Mirror]",
            "options": [
                "A) 1 letter",
                "B) 2 letters",
                "C) 3 letters",
                "D) 4 letters"
            ],
            "answer": "C) 3 letters",
            "explanation": "Letters with vertical symmetry look identical under vertical reflection:\n• N: Changes laterally\n• A: Symmetric (identical)\n• V: Symmetric (identical)\n• A: Symmetric (identical)\n• L: Changes laterally\nTotal symmetric invariant letters = **3** ('A', 'V', 'A')."
        },
        {
            "id": 15,
            "category": "Direction & Relative Positioning",
            "question": "A person walks **12 km North**, turns right and walks **9 km East**, and finally turns right and walks **12 km South**. How far and in what direction is the person from their starting point?",
            "visual": "12 km North  -->  9 km East  -->  12 km South",
            "options": [
                "A) 9 km East",
                "B) 15 km North-East",
                "C) 9 km West",
                "D) 12 km South"
            ],
            "answer": "A) 9 km East",
            "explanation": "The 12 km North and 12 km South cancel each other along the North-South axis. The net displacement is strictly **9 km East** of the starting point."
        },
        {
            "id": 16,
            "category": "Series Completion (Multipliers)",
            "question": "Identify the missing value in this progression: \n\n**2,  3,  6,  15,  45,  ?**",
            "visual": None,
            "options": [
                "A) 90",
                "B) 135",
                "C) 157.5",
                "D) 180"
            ],
            "answer": "C) 157.5",
            "explanation": "The multiplier increases by 0.5 at each consecutive step:\n• 2 × 1.5 = 3\n• 3 × 2.0 = 6\n• 6 × 2.5 = 15\n• 15 × 3.0 = 45\n• 45 × 3.5 = **157.5**."
        },
        {
            "id": 17,
            "category": "Logical Sequence",
            "question": "Arrange these five steps in a logical chronological sequence:\n\n1. Target Identification\n2. Action Execution\n3. Initial Contact / Detection\n4. Performance Review\n5. Departure & Start",
            "visual": None,
            "options": [
                "A) 5, 3, 1, 2, 4",
                "B) 3, 1, 5, 2, 4",
                "C) 5, 1, 3, 2, 4",
                "D) 1, 3, 5, 2, 4"
            ],
            "answer": "A) 5, 3, 1, 2, 4",
            "explanation": "The logical sequence is:\nDeparture & Start (5) → Initial Contact / Detection (3) → Target Identification (1) → Action Execution (2) → Performance Review (4)."
        },
        {
            "id": 18,
            "category": "Verbal Reasoning (Relations)",
            "question": "Pointing to a photograph of a man, Varun said: *'His father is the only son of my father.'* How is Varun related to the man in the photograph?",
            "visual": None,
            "options": [
                "A) Brother",
                "B) Father",
                "C) Uncle",
                "D) Grandfather"
            ],
            "answer": "B) Father",
            "explanation": "'The only son of my father' refers directly to Varun himself. Therefore, the man's father is Varun, meaning Varun is his **Father**."
        },
        {
            "id": 19,
            "category": "Calendar Logic",
            "question": "If the day after tomorrow is **Tuesday**, which day of the week was **two days before yesterday**?",
            "visual": None,
            "options": [
                "A) Wednesday",
                "B) Thursday",
                "C) Friday",
                "D) Saturday"
            ],
            "answer": "B) Thursday",
            "explanation": "• If day after tomorrow is Tuesday, then tomorrow is Monday, and **Today is Sunday**.\n• Yesterday was Saturday.\n• Two days before Saturday was **Thursday**."
        },
        {
            "id": 20,
            "category": "Spatial Aptitude (Die Rotation)",
            "question": "Two positions of the same die are observed:\n• **Position 1:** Top = 1, Front = 2, Right = 3\n• **Position 2:** Top = 1, Front = 3, Right = 5\n\nWhich face is **directly opposite to Face 2**?",
            "visual": """
Position 1:   [Top: 1] | [Front: 2] | [Right: 3]
Position 2:   [Top: 1] | [Front: 3] | [Right: 5]""",
            "options": [
                "A) Face 4",
                "B) Face 5",
                "C) Face 6",
                "D) Face 1"
            ],
            "answer": "B) Face 5",
            "explanation": "Face 1 remains at the top. The die has been rotated 90° counter-clockwise around the vertical axis. Face 3 moves from the right to the front, which means the back face rotates to the right (Face 5). Therefore, Face 5 is directly opposite Face 2."
        }
    ]


def get_coding_decoding_pyq_bank():
    """
    Returns exactly 20 authentic Previous Year Questions (PYQs) from SSB OIR / AFCAT / CDS
    on the single most mandatory and highest-weightage topic: Coding & Decoding.
    """
    return [
        {
            "id": 1,
            "category": "Coding & Decoding (Forward Letter Shift)",
            "question": "In a certain code language, if **MADRAS** is coded as **NBESBT**, how will **BOMBAY** be coded in that same system?",
            "visual": "M(+1)=N, A(+1)=B, D(+1)=E, R(+1)=S, A(+1)=B, S(+1)=T",
            "options": [
                "A) CPNCBZ",
                "B) CPOCBZ",
                "C) CQOCBZ",
                "D) BQNCBZ"
            ],
            "answer": "A) CPNCBZ",
            "explanation": "Each letter in the word is shifted forward by +1 alphabetical position:\n• B (+1) = C\n• O (+1) = P\n• M (+1) = N\n• B (+1) = C\n• A (+1) = B\n• Y (+1) = Z\nCombining these yields **CPNCBZ**."
        },
        {
            "id": 2,
            "category": "Coding & Decoding (Constant Forward Shift)",
            "question": "If **TEACHER** is written as **VGCEJGT** in a code language, how will **CHILDREN** be coded under the exact same rule?",
            "visual": "T(+2)=V, E(+2)=G, A(+2)=C, C(+2)=E, H(+2)=J, E(+2)=G, R(+2)=T",
            "options": [
                "A) EJKNFTGP",
                "B) EJKNEGHP",
                "C) EJKNFUHP",
                "D) EJKNFTGO"
            ],
            "answer": "A) EJKNFTGP",
            "explanation": "Every letter moves forward by +2 alphabetical steps:\n• C (+2) = E\n• H (+2) = J\n• I (+2) = K\n• L (+2) = N\n• D (+2) = F\n• R (+2) = T\n• E (+2) = G\n• N (+2) = P\nResult = **EJKNFTGP**."
        },
        {
            "id": 3,
            "category": "Coding & Decoding (Reverse Shift / Decryption)",
            "question": "If in a secret transmission, **COVET** is encoded as **FRYHW**, which original plaintext word was encoded to produce **SHDUO**?",
            "visual": "Encoding rule: +3 forward  |  Decoding rule: -3 backward",
            "options": [
                "A) PEARL",
                "B) REPAY",
                "C) PEAKY",
                "D) STARE"
            ],
            "answer": "A) PEARL",
            "explanation": "Forward coding rule adds +3 to each letter (C+3=F, O+3=R, V+3=Y, E+3=H, T+3=W).\nTo decode SHDUO back to the original word, subtract 3 (-3) from each letter:\n• S (19) - 3 = 16 (P)\n• H (8) - 3 = 5 (E)\n• D (4) - 3 = 1 (A)\n• U (21) - 3 = 18 (R)\n• O (15) - 3 = 12 (L)\nThe original word is **PEARL**."
        },
        {
            "id": 4,
            "category": "Coding & Decoding (Reverse Sequence Shift)",
            "question": "In a code language, **MONKEY** is written as **XDJMNL**. How will **TIGER** be coded in that same language?",
            "visual": "Last to first with -1: Y(-1)=X, E(-1)=D, K(-1)=J, N(-1)=M, O(-1)=N, M(-1)=L",
            "options": [
                "A) QDFHS",
                "B) SDFHQ",
                "C) SHFDQ",
                "D) UJHFS"
            ],
            "answer": "A) QDFHS",
            "explanation": "The pattern reads the original word in reverse order from the last letter to the first, subtracting 1 (-1) from each letter:\n• R (-1) = Q\n• E (-1) = D\n• G (-1) = F\n• I (-1) = H\n• T (-1) = S\nCombining from the last to first gives **QDFHS**."
        },
        {
            "id": 5,
            "category": "Coding & Decoding (Sectional Inversion)",
            "question": "If **SYSTEM** is coded as **SYSMET** and **NEARER** is coded as **AENRER**, how will the word **FRACTION** be coded?",
            "visual": "FRAC | TION  -->  Reverse 1st half | Reverse 2nd half",
            "options": [
                "A) CARFNOIT",
                "B) CRAFNOIT",
                "C) NOITCARF",
                "D) CARFTION"
            ],
            "answer": "A) CARFNOIT",
            "explanation": "The word is divided into two equal halves of 4 letters each:\n• First half 'FRAC' reversed becomes 'CARF'.\n• Second half 'TION' reversed becomes 'NOIT'.\nMerging both halves results in **CARFNOIT**."
        },
        {
            "id": 6,
            "category": "Coding & Decoding (Reverse Alphabet Pairs)",
            "question": "If **CERTAIN** is coded as **XVIGZRM** (where A↔Z, B↔Y, C↔X...), how will the word **REQUIRED** be coded?",
            "visual": "Opposite Pair Rule: Letter Rank + Opposite Rank = 27",
            "options": [
                "A) IVJFRIVW",
                "B) IVJFQIVW",
                "C) JVIFRIVW",
                "D) IVJFSIUW"
            ],
            "answer": "A) IVJFRIVW",
            "explanation": "Each letter is replaced by its complementary opposite letter from the alphabet (positions sum to 27):\n• R (18) ↔ I (9)\n• E (5) ↔ V (22)\n• Q (17) ↔ J (10)\n• U (21) ↔ F (6)\n• I (9) ↔ R (18)\n• R (18) ↔ I (9)\n• E (5) ↔ V (22)\n• D (4) ↔ W (23)\nResult = **IVJFRIVW**."
        },
        {
            "id": 7,
            "category": "Coding & Decoding (Direct Digit Substitution)",
            "question": "If **DELHI** is coded as **73541** and **CALCUTTA** is coded as **82589662**, how will **CALICUT** be written in that code?",
            "visual": "C=8, A=2, L=5, I=1, U=9, T=6",
            "options": [
                "A) 8251896",
                "B) 8251869",
                "C) 8258196",
                "D) 8521896"
            ],
            "answer": "A) 8251896",
            "explanation": "Each letter directly maps to a fixed numeral established in the sample words:\n• C = 8\n• A = 2\n• L = 5\n• I = 1\n• C = 8\n• U = 9\n• T = 6\nAssembling the digits for CALICUT produces **8251896**."
        },
        {
            "id": 8,
            "category": "Coding & Decoding (Alphabetical Positional Sum)",
            "question": "In a military cipher system, if **D = 4**, **BAD = 7**, and **COVER = 63**, what is the numerical code value for **BASIS**?",
            "visual": "Rule: Sum of standard alphabetical ranks (A=1, B=2, ..., Z=26)",
            "options": [
                "A) 48",
                "B) 50",
                "C) 52",
                "D) 54"
            ],
            "answer": "B) 50",
            "explanation": "The code equals the direct arithmetic sum of the alphabetical positions:\n• B = 2\n• A = 1\n• S = 19\n• I = 9\n• S = 19\nTotal = 2 + 1 + 19 + 9 + 19 = **50**."
        },
        {
            "id": 9,
            "category": "Coding & Decoding (Reverse Alphabetical Sum)",
            "question": "If **GO = 32** and **SHE = 49**, what will be the coded numerical value for **SOME** in that same language?",
            "visual": "Reverse rank values: A=26, B=25, ..., Z=1  (Formula: 27 - Rank)",
            "options": [
                "A) 54",
                "B) 56",
                "C) 58",
                "D) 62"
            ],
            "answer": "B) 56",
            "explanation": "The numerical code is the sum of the reverse alphabetical positions (27 - standard rank):\n• S: 27 - 19 = 8\n• O: 27 - 15 = 12\n• M: 27 - 13 = 14\n• E: 27 - 5 = 22\nSum = 8 + 12 + 14 + 22 = **56**."
        },
        {
            "id": 10,
            "category": "Coding & Decoding (Progressive Increment)",
            "question": "In a certain code, **EARTH** is written as **FCUXM**. How will the word **SUPER** be written in that code?",
            "visual": "Consecutive letter shifts: +1, +2, +3, +4, +5",
            "options": [
                "A) TWSIW",
                "B) TVSIW",
                "C) TWRIW",
                "D) TXSJW"
            ],
            "answer": "A) TWSIW",
            "explanation": "The forward shift increments by +1 for each successive position:\n• S (19) + 1 = 20 (T)\n• U (21) + 2 = 23 (W)\n• P (16) + 3 = 19 (S)\n• E (5) + 4 = 9 (I)\n• R (18) + 5 = 23 (W)\nResult = **TWSIW**."
        },
        {
            "id": 11,
            "category": "Coding & Decoding (Alternating Direction Shifts)",
            "question": "If **STUDENT** is coded as **RUTEDOS**, how will **OFFICER** be coded under the exact same pattern?",
            "visual": "Shift pattern: -1, +1, -1, +1, -1, +1, -1",
            "options": [
                "A) NGEJBFQ",
                "B) PFEJBFQ",
                "C) NGEIBFQ",
                "D) NGEJCFQ"
            ],
            "answer": "A) NGEJBFQ",
            "explanation": "The transformation alternates between -1 and +1:\n• O (-1) = N\n• F (+1) = G\n• F (-1) = E\n• I (+1) = J\n• C (-1) = B\n• E (+1) = F\n• R (-1) = Q\nResult = **NGEJBFQ**."
        },
        {
            "id": 12,
            "category": "Coding & Decoding (Common Message Deduction)",
            "question": "In an intercepted cipher transmission:\n• **'pit dar na'** means **'you are good'**\n• **'dar tok pa'** means **'good and bad'**\n• **'na tim tok'** means **'they are bad'**\n\nWhich specific code word stands for **'they'**?",
            "visual": "Isolate common words across statements: dar=good, na=are, tok=bad",
            "options": [
                "A) na",
                "B) tok",
                "C) tim",
                "D) dar"
            ],
            "answer": "C) tim",
            "explanation": "• Sentences 1 & 2 share 'dar' and 'good' → **dar = good**\n• Sentences 1 & 3 share 'na' and 'are' → **na = are**\n• Sentences 2 & 3 share 'tok' and 'bad' → **tok = bad**\nIn sentence 3 ('na tim tok' = 'they are bad'), na='are' and tok='bad'. The remaining word **tim** must represent **they**."
        },
        {
            "id": 13,
            "category": "Coding & Decoding (Artificial Substitution)",
            "question": "If **'light'** is called **'morning'**, **'morning'** is called **'dark'**, **'dark'** is called **'night'**, **'night'** is called **'sunshine'**, and **'sunshine'** is called **'dusk'**, when do people normally sleep at bedtime?",
            "visual": "Normal time = 'night'  -->  Coded substitution = 'sunshine'",
            "options": [
                "A) dark",
                "B) night",
                "C) sunshine",
                "D) dusk"
            ],
            "answer": "C) sunshine",
            "explanation": "In ordinary reality, people sleep during the **night**.\nUnder the given coding chain, **'night'** is called **'sunshine'**.\nHence, the correct coded answer is **sunshine**."
        },
        {
            "id": 14,
            "category": "Coding & Decoding (Functional Rank Transform)",
            "question": "If **ACNE** is encoded as **3, 7, 29, 11**, what will be the coded numerical representation for **BOIL**?",
            "visual": "Formula: Code = (2 × Alphabetical Rank) + 1",
            "options": [
                "A) 5, 31, 19, 25",
                "B) 5, 29, 19, 25",
                "C) 4, 30, 18, 24",
                "D) 5, 31, 21, 27"
            ],
            "answer": "A) 5, 31, 19, 25",
            "explanation": "Each letter's alphabetical rank $n$ is transformed by the formula $2n + 1$:\n• A(1) → 2(1)+1 = 3\n• C(3) → 2(3)+1 = 7\n• N(14) → 2(14)+1 = 29\n• E(5) → 2(5)+1 = 11\nApplying $2n + 1$ to **BOIL**:\n• B(2) → 2(2)+1 = **5**\n• O(15) → 2(15)+1 = **31**\n• I(9) → 2(9)+1 = **19**\n• L(12) → 2(12)+1 = **25**\nResult = **5, 31, 19, 25**."
        },
        {
            "id": 15,
            "category": "Coding & Decoding (Pairwise Position Swap)",
            "question": "In a cryptographic protocol, **COMBAT** is coded as **OCBMTA**. How will the patrol reconnaissance word **PATROL** be coded under this protocol?",
            "visual": "(PA)(TR)(OL)  -->  (AP)(RT)(LO)",
            "options": [
                "A) APRTLO",
                "B) APTROL",
                "C) APORTL",
                "D) LORTAP"
            ],
            "answer": "A) APRTLO",
            "explanation": "Adjacent letter pairs are swapped:\n• Letters 1 & 2: PA → **AP**\n• Letters 3 & 4: TR → **RT**\n• Letters 5 & 6: OL → **LO**\nCombining these yields **APRTLO**."
        },
        {
            "id": 16,
            "category": "Coding & Decoding (Direct Symbol Mapping)",
            "question": "In an encrypted tactical dispatch:\n• **BRAKE** is written as **% # * ? @**\n• **MOTOR** is written as **$ + ! + #**\n\nHow is the target word **ROBOT** represented in that code?",
            "visual": "R=#, O=+, B=%, O=+, T=!",
            "options": [
                "A) # + % + !",
                "B) # % + + !",
                "C) # + % ! +",
                "D) ! + % + #"
            ],
            "answer": "A) # + % + !",
            "explanation": "Extract individual symbol mappings:\n• R = **#** (from BRAKE and MOTOR)\n• O = **+** (from MOTOR)\n• B = **%** (from BRAKE)\n• O = **+** (from MOTOR)\n• T = **!** (from MOTOR)\nArranging for ROBOT yields **# + % + !**."
        },
        {
            "id": 17,
            "category": "Coding & Decoding (Positional Product by Length)",
            "question": "If **CAT = 72** and **MAN = 84**, what is the coded numerical value for **LION**?",
            "visual": "Formula: Code = (Sum of alphabetical ranks) × (Total number of letters)",
            "options": [
                "A) 180",
                "B) 190",
                "C) 200",
                "D) 210"
            ],
            "answer": "C) 200",
            "explanation": "Rule: (Sum of letter positions) × (Number of letters):\n• CAT: (3 + 1 + 20) × 3 = 24 × 3 = 72\n• MAN: (13 + 1 + 14) × 3 = 28 × 3 = 84\n• LION: L(12) + I(9) + O(15) + N(14) = 50. Length = 4 letters.\nCode = 50 × 4 = **200**."
        },
        {
            "id": 18,
            "category": "Coding & Decoding (Uniform Decrement Shift)",
            "question": "In a defensive transmission, if **ROBUST** is coded as **QNATRS**, how will **VICTOR** be encoded under the same rule?",
            "visual": "V(-1)=U, I(-1)=H, C(-1)=B, T(-1)=S, O(-1)=N, R(-1)=Q",
            "options": [
                "A) UHBSNQ",
                "B) UHBTMQ",
                "C) THBSNQ",
                "D) UHBSNR"
            ],
            "answer": "A) UHBSNQ",
            "explanation": "Every letter is shifted backward by 1 position (-1):\n• V (-1) = **U**\n• I (-1) = **H**\n• C (-1) = **B**\n• T (-1) = **S**\n• O (-1) = **N**\n• R (-1) = **Q**\nResult = **UHBSNQ**."
        },
        {
            "id": 19,
            "category": "Coding & Decoding (Progressive Variable Shift)",
            "question": "If **GAMBLE** is coded as **HCPFQK** (with shifts of +1, +2, +3, +4, +5, +6), what will be the code for **DEFENCE** under this progressive shift (+1 through +7)?",
            "visual": "D(+1), E(+2), F(+3), E(+4), N(+5), C(+6), E(+7)",
            "options": [
                "A) EGIISIL",
                "B) EGIIQIL",
                "C) FGJJTJM",
                "D) EGHISIK"
            ],
            "answer": "A) EGIISIL",
            "explanation": "The shift increases by 1 for each letter position:\n• D (4) + 1 = 5 (E)\n• E (5) + 2 = 7 (G)\n• F (6) + 3 = 9 (I)\n• E (5) + 4 = 9 (I)\n• N (14) + 5 = 19 (S)\n• C (3) + 6 = 9 (I)\n• E (5) + 7 = 12 (L)\nResult = **EGIISIL**."
        },
        {
            "id": 20,
            "category": "Coding & Decoding (Digital Root of Letter Ranks)",
            "question": "If in a special code, **HARYANA** is coded as **8197151** (where double-digit positions are reduced by digit sum, e.g. R=18 → 1+8=9, Y=25 → 2+5=7, N=14 → 1+4=5), how will **DELHI** be coded?",
            "visual": "D(4)=4, E(5)=5, L(12)->1+2=3, H(8)=8, I(9)=9",
            "options": [
                "A) 45389",
                "B) 45189",
                "C) 45289",
                "D) 35389"
            ],
            "answer": "A) 45389",
            "explanation": "Single-digit letters keep their rank ($D=4, E=5, H=8, I=9$). Double-digit ranks are summed:\n• L is 12 → 1 + 2 = **3**\nAssembling all digits for DELHI produces **45389**."
        }
    ]


def get_clocks_and_calendar_pyq_bank():
    """
    Returns exactly 20 authentic Previous Year Questions (PYQs) from SSB Interview
    NAOO (Naval Air Operations Officer / Observer) Entry OIR Test
    covering the high-weightage topics: Clocks & Calendar.
    """
    return [
        {
            "id": 1,
            "category": "SSB OIR • Clocks (Angle Between Hands)",
            "question": "An officer candidate at INS Garuda checks the cockpit analog clock at **08:30 hrs (8:30 AM)** during pre-flight briefing. What is the angle between the hour hand and the minute hand?",
            "visual": "Angle Formula: θ = |30H - (11/2)M|  -->  H = 8, M = 30",
            "options": [
                "A) 65°",
                "B) 75°",
                "C) 80°",
                "D) 85°"
            ],
            "answer": "B) 75°",
            "explanation": "Using standard clock angle formula:\n• $\\theta = |30H - \\frac{11}{2}M|$\n• For $H = 8$ and $M = 30$:\n• $\\theta = |30(8) - \\frac{11}{2}(30)| = |240 - 165| = 75^\\circ$.\n\nHence, the angle between the hour and minute hands at 8:30 is **75°**."
        },
        {
            "id": 2,
            "category": "SSB OIR • Clocks (Coinciding Hands)",
            "question": "During a naval navigation exercise, at what exact time between **4 o'clock and 5 o'clock** will the hour hand and the minute hand of the chronometer coincide (0° angle)?",
            "visual": "At H o'clock, hands coincide at M = (60/11) × H minutes past H",
            "options": [
                "A) 21 9/11 min past 4",
                "B) 22 min past 4",
                "C) 20 4/11 min past 4",
                "D) 23 2/11 min past 4"
            ],
            "answer": "A) 21 9/11 min past 4",
            "explanation": "The minute hand gains 55 minutes spaces over the hour hand in 60 minutes (ratio = $\\frac{60}{55} = \\frac{12}{11}$):\n• At 4 o'clock, the hour hand is 20 minute spaces ahead.\n• To coincide, the minute hand must gain 20 spaces: $20 \\times \\frac{12}{11} = \\frac{240}{11} = 21 \\frac{9}{11}$ minutes.\n\nAlternatively, using $\\theta = |30H - \\frac{11}{2}M| = 0$:\n• $30(4) = \\frac{11}{2}M \\implies 120 = \\frac{11}{2}M \\implies M = \\frac{240}{11} = 21 \\frac{9}{11}$ min.\n\nThus, the hands coincide at **21 9/11 min past 4**."
        },
        {
            "id": 3,
            "category": "SSB OIR • Clocks (Hour Hand Angular Displacement)",
            "question": "A naval ship's bridge clock shows **0800 hrs (8:00 AM)** as the vessel leaves harbour. Through how many degrees will the hour hand rotate when the clock reads **1400 hrs (2:00 PM)** on the same day?",
            "visual": "08:00 AM to 02:00 PM = 6 Hours  |  Hour hand moves 30° per hour",
            "options": [
                "A) 150°",
                "B) 165°",
                "C) 180°",
                "D) 210°"
            ],
            "answer": "C) 180°",
            "explanation": "• Total elapsed time from 8:00 AM to 2:00 PM = 6 hours.\n• The hour hand makes a full $360^\\circ$ rotation in 12 hours, meaning it turns $\\frac{360^\\circ}{12} = 30^\\circ$ each hour (or $0.5^\\circ$ per minute).\n• Angular displacement = $6 \\times 30^\\circ = 180^\\circ$.\n\nTherefore, the hour hand rotates through **180°**."
        },
        {
            "id": 4,
            "category": "SSB OIR • Clocks (Opposite Direction Hands)",
            "question": "At what time between **7 o'clock and 8 o'clock** are the hands of a clock pointing in diametrically opposite directions (forming a straight line of 180°)?",
            "visual": "θ = 180°  -->  M = (2/11) × |30H - 180| for H = 7",
            "options": [
                "A) 5 5/11 min past 7",
                "B) 5 min past 7",
                "C) 6 2/11 min past 7",
                "D) 5 8/11 min past 7"
            ],
            "answer": "A) 5 5/11 min past 7",
            "explanation": "At 7 o'clock, the hour hand is at 35 minute spaces (or $210^\\circ$).\n• For opposite direction (180°), the hands must be separated by 30 minute spaces.\n• Since the hour hand is ahead of the 30-space mark, the minute hand needs to be at $35 - 30 = 5$ minute spaces.\n• Time required to gain 5 minute spaces = $5 \\times \\frac{12}{11} = \\frac{60}{11} = 5 \\frac{5}{11}$ minutes.\n\nUsing formula: $M = \\frac{2}{11}(30 \\times 7 - 180) = \\frac{2}{11}(210 - 180) = \\frac{2}{11}(30) = \\frac{60}{11} = 5 \\frac{5}{11}$ min.\n\nThus, hands are in opposite directions at **5 5/11 min past 7**."
        },
        {
            "id": 5,
            "category": "SSB OIR • Clocks (Mirror Image Reflection)",
            "question": "An observer candidate observes an analog clock dial through the periscope's reflective mirror, which shows the apparent time as **03:40**. What is the actual true time?",
            "visual": "Mirror Image Formula: Actual Time = 11:60 - Mirror Time",
            "options": [
                "A) 8:40",
                "B) 9:20",
                "C) 7:20",
                "D) 8:20"
            ],
            "answer": "D) 8:20",
            "explanation": "To determine the actual time from a vertical mirror reflection:\n• Subtract the reflected time from 11:60 (or 23:60 for 24-hr clock):\n  $$\\text{Actual Time} = 11:60 - 03:40 = 08:20$$\n\nTherefore, the true time displayed on the clock is **8:20**."
        },
        {
            "id": 6,
            "category": "SSB OIR • Clocks (Hands in a Straight Line)",
            "question": "In a complete 24-hour operational cycle of a naval base, how many times do the hands of a clock form a **straight line**?",
            "visual": "Straight Line = Hands Coinciding (0°) + Hands Opposite (180°)",
            "options": [
                "A) 22 times",
                "B) 24 times",
                "C) 44 times",
                "D) 48 times"
            ],
            "answer": "C) 44 times",
            "explanation": "Hands are in a 'straight line' in two conditions:\n1. When they **coincide (0°)**: Occurs 11 times in 12 hours (coincides only once between 11 and 1), which is $11 \\times 2 = 22$ times in 24 hours.\n2. When they are **diametrically opposite (180°)**: Occurs 11 times in 12 hours (opposite only once between 5 and 7), which is $11 \\times 2 = 22$ times in 24 hours.\n\n• Total occurrences in a straight line in 24 hours = $22 + 22 = 44$ times."
        },
        {
            "id": 7,
            "category": "SSB OIR • Clocks (Right Angles in 24 Hours)",
            "question": "During a 24-hour maritime watchkeeping duty, how many times are the hour hand and minute hand of a clock at right angles (**90°**) to each other?",
            "visual": "Right Angles (90°): 2 times/hr nominally, but 44 times in 24 hours",
            "options": [
                "A) 22 times",
                "B) 44 times",
                "C) 48 times",
                "D) 88 times"
            ],
            "answer": "B) 44 times",
            "explanation": "In general, clock hands are at right angles ($90^\\circ$) twice every hour.\n• However, in a 12-hour period, between 2–4 and 8–10 o'clock, the right angles occur only 3 times each instead of 4 (with 3:00 and 9:00 being common shared points).\n• Right angles in 12 hours = $22$ times.\n• Right angles in 24 hours = $22 \\times 2 = 44$ times.\n\nHence, the hands form a right angle **44 times** in 24 hours."
        },
        {
            "id": 8,
            "category": "SSB OIR • Clocks (Reflex Angle Calculation)",
            "question": "What is the **reflex angle** between the hands of a clock at **10:25**?",
            "visual": "Angle θ = |30H - (11/2)M|  |  Reflex Angle = 360° - θ",
            "options": [
                "A) 162.5°",
                "B) 180°",
                "C) 205.5°",
                "D) 197.5°"
            ],
            "answer": "D) 197.5°",
            "explanation": "First calculate the interior angle $\\theta$ between the hands at $H = 10$, $M = 25$:\n• $\\theta = |30(10) - \\frac{11}{2}(25)| = |300 - 137.5| = 162.5^\\circ$\n• By definition, a reflex angle is greater than $180^\\circ$ and less than $360^\\circ$:\n• $\\text{Reflex Angle} = 360^\\circ - 162.5^\\circ = 197.5^\\circ$ (or $197 \\frac{1}{2}^\\circ$).\n\nThus, the reflex angle is **197.5°**."
        },
        {
            "id": 9,
            "category": "SSB OIR • Clocks (Faulty Gaining Clock)",
            "question": "A mechanical chronometer gains **5 seconds every 3 minutes**. It is synchronized correctly at **07:00 AM**. What is the true time when the chronometer displays **04:15 PM** on the same day?",
            "visual": "Chronometer runs 3 min 5 sec (37/12 min) for every 3 min of true time",
            "options": [
                "A) 3:45 PM",
                "B) 4:00 PM",
                "C) 4:05 PM",
                "D) 4:10 PM"
            ],
            "answer": "B) 4:00 PM",
            "explanation": "1. Elapsed time on the fast watch from 7:00 AM to 4:15 PM:\n• $9\\text{ hrs } 15\\text{ min} = (9 \\times 60) + 15 = 555\\text{ minutes}$.\n\n2. Gain rate:\n• In $3\\text{ min}$ true time, watch shows $3\\text{ min } 5\\text{ s} = 3 + \\frac{5}{60} = 3 + \\frac{1}{12} = \\frac{37}{12}\\text{ minutes}$.\n• So $\\frac{37}{12}$ watch minutes = $3$ true minutes.\n• $1$ watch minute = $3 \\times \\frac{12}{37} = \\frac{36}{37}$ true minutes.\n\n3. True time for 555 watch minutes:\n• $\\text{True minutes} = 555 \\times \\frac{36}{37} = 15 \\times 36 = 540\\text{ minutes} = 9\\text{ hours}$.\n\n• True time = $7:00\\text{ AM} + 9\\text{ hours} =$ **4:00 PM**."
        },
        {
            "id": 10,
            "category": "SSB OIR • Clocks (Coincidence Rate & Error)",
            "question": "The hands of an analog clock coincide every **64 minutes** of true time. How much time does the clock lose or gain in a 24-hour day?",
            "visual": "Normal Coincidence = 65 (5/11) min  |  Observed = 64 min  -->  Clock is FAST",
            "options": [
                "A) 32 8/11 min loss",
                "B) 36 5/11 min gain",
                "C) 30 min gain",
                "D) 32 8/11 min gain"
            ],
            "answer": "D) 32 8/11 min gain",
            "explanation": "In an accurate clock, hands coincide every $\\frac{720}{11} = 65 \\frac{5}{11}$ minutes.\n• Since the hands coincide every 64 minutes (faster than standard), the clock is **gaining time**.\n• Gain in 64 minutes = $\\left(65 \\frac{5}{11} - 64\\right) = \\frac{16}{11}$ minutes.\n• Gain per minute = $\\frac{16}{11 \\times 64} = \\frac{1}{44}$ minute.\n• Total gain in 24 hours ($24 \\times 60 = 1440$ minutes):\n  $$\\text{Gain} = 1440 \\times \\frac{1}{44} = \\frac{360}{11} = 32 \\frac{8}{11}\\text{ minutes}$$\n\nHence, the clock gains **32 8/11 min** in 24 hours."
        },
        {
            "id": 11,
            "category": "SSB OIR • Calendar (Historical Day of Week)",
            "question": "India attained Independence on **15th August 1947**. On which day of the week did this historic event occur?",
            "visual": "Formula / Hint: 1600 yrs = 0 odd days | 300 yrs = 1 odd day | Odd days in 46 completed years (11 leap + 35 ord) + Jan-Aug 15 days",
            "options": [
                "A) Thursday",
                "B) Friday",
                "C) Saturday",
                "D) Wednesday"
            ],
            "answer": "B) Friday",
            "explanation": "Step-by-step Odd Days Calculation:\n1. 1600 years: 0 odd days.\n2. 300 years (1601 to 1900): 1 odd day.\n3. 46 completed years (1901 to 1946):\n• Leap years = $46 // 4 = 11$.\n• Ordinary years = $46 - 11 = 35$.\n• Odd days = $(11 \\times 2) + (35 \\times 1) = 22 + 35 = 57 \\equiv 1\\text{ odd day } (57 \\pmod 7)$.\n\n4. Days in 1947 (up to 15 Aug):\n• Jan(3) + Feb(0) + Mar(3) + Apr(2) + May(3) + Jun(2) + Jul(3) + Aug 15(1) = 17 days $\\equiv 3\\text{ odd days}$.\n\n5. Total odd days = $1 + 1 + 3 = 5\\text{ odd days}$.\n• Day code 5 corresponds to **Friday** (0=Sun, 1=Mon, ..., 5=Fri)."
        },
        {
            "id": 12,
            "category": "SSB OIR • Calendar (Repetition of Calendar)",
            "question": "A naval officer is cataloguing annual operational logs. Which future year will have the exact same calendar as the year **2007**?",
            "visual": "Calendar Repeat Rule: Leap+1 (+6 yrs), Leap+2/3 (+11 yrs), Leap (+28 yrs)",
            "options": [
                "A) 2014",
                "B) 2016",
                "C) 2018",
                "D) 2020"
            ],
            "answer": "C) 2018",
            "explanation": "Standard Calendar Repetition Rules:\n• A leap year repeats after 28 years.\n• Year immediately after leap year (Leap + 1) repeats after 6 years.\n• Years that are (Leap + 2) or (Leap + 3) repeat after **11 years**.\n\nSince 2004 was a leap year, 2007 is (Leap + 3):\n• $2007 + 11 = 2018$.\n\nVerifying odd days:\n2007(1) + 2008(2) + 2009(1) + 2010(1) + 2011(1) + 2012(2) + 2013(1) + 2014(1) + 2015(1) + 2016(2) + 2017(1) = 14 odd days $\\equiv 0\\pmod 7$.\nSince 2018 is also an ordinary year, **2018** has the identical calendar to 2007."
        },
        {
            "id": 13,
            "category": "SSB OIR • Calendar (Relative Day Deduction)",
            "question": "If the **day before yesterday was Thursday**, what day of the week will it be **four days after tomorrow**?",
            "visual": "Formula / Hint: Work step-by-step from 'Day before yesterday' to determine 'Today', then project forward 4 days after tomorrow",
            "options": [
                "A) Wednesday",
                "B) Thursday",
                "C) Friday",
                "D) Saturday"
            ],
            "answer": "B) Thursday",
            "explanation": "Break down the timeline relative to Today:\n• Day before yesterday = Thursday\n• Yesterday = Friday\n• **Today = Saturday**\n• Tomorrow = Sunday\n• Four days after tomorrow = Sunday + 4 days = **Thursday**.\n\nThus, the resulting day is **Thursday**."
        },
        {
            "id": 14,
            "category": "SSB OIR • Calendar (Century Last Day Properties)",
            "question": "Based on the mathematical principles of the Gregorian calendar, which of the following days **can never be the last day of a century**?",
            "visual": "Century Odd Days: 100 yr=5 (Fri), 200 yr=3 (Wed), 300 yr=1 (Mon), 400 yr=0 (Sun)",
            "options": [
                "A) Tuesday",
                "B) Wednesday",
                "C) Friday",
                "D) Sunday"
            ],
            "answer": "A) Tuesday",
            "explanation": "Odd days at the close of centuries:\n• 100 years = 5 odd days $\\rightarrow$ **Friday**\n• 200 years = 3 odd days $\\rightarrow$ **Wednesday**\n• 300 years = 1 odd day $\\rightarrow$ **Monday**\n• 400 years = 0 odd days $\\rightarrow$ **Sunday**\n\nThe last day of a century can ONLY be Friday, Wednesday, Monday, or Sunday.\n\nTherefore, **Tuesday**, **Thursday**, and **Saturday** can NEVER be the last day of a century."
        },
        {
            "id": 15,
            "category": "SSB OIR • Calendar (Odd Days in 400 Years)",
            "question": "How many **odd days** are accumulated over a continuous span of **400 consecutive years**?",
            "visual": "(100 yrs × 4) + 1 leap century day = (5 × 4) + 1 = 21 days ≡ 0 odd days",
            "options": [
                "A) 0",
                "B) 1",
                "C) 3",
                "D) 5"
            ],
            "answer": "A) 0",
            "explanation": "• A normal 100-year span contains 76 ordinary years and 24 leap years:\n  $(76 \\times 1) + (24 \\times 2) = 124\\text{ days} = 17\\text{ weeks } + 5\\text{ odd days}$.\n• In 400 years, there are $4 \\times 100\\text{-year periods}$, plus 1 extra day because the 400th year is a leap century year:\n• Total odd days = $(5 \\times 4) + 1 = 21\\text{ days}$.\n• Since $21 \\div 7 = 3$ exact weeks with remainder 0, there are **0 odd days** in 400 years."
        },
        {
            "id": 16,
            "category": "SSB OIR • Calendar (Year-to-Year Shift)",
            "question": "If **1st January 2006** was a **Sunday**, what day of the week was **1st January 2010**?",
            "visual": "Formula / Hint: Ordinary year = 1 odd day (+1) | Leap year = 2 odd days (+2). Sum odd days from 2006 to 2009 and add to Sunday",
            "options": [
                "A) Friday",
                "B) Thursday",
                "C) Saturday",
                "D) Sunday"
            ],
            "answer": "A) Friday",
            "explanation": "Count odd days for each elapsed year:\n• 2006 (ordinary year) = 1 odd day\n• 2007 (ordinary year) = 1 odd day\n• 2008 (leap year) = 2 odd days\n• 2009 (ordinary year) = 1 odd day\n\nTotal odd days from 1 Jan 2006 to 1 Jan 2010 = $1 + 1 + 2 + 1 = 5$ odd days.\n• Sunday + 5 days = **Friday**."
        },
        {
            "id": 17,
            "category": "SSB OIR • Calendar (Intra-Year Month Shift)",
            "question": "In a standard non-leap year, if **15th March** fell on a **Wednesday**, what day of the week was **15th August** in that same year?",
            "visual": "Remaining March(16) + Apr(30) + May(31) + Jun(30) + Jul(31) + Aug(15) = 153 days ≡ 6 mod 7",
            "options": [
                "A) Monday",
                "B) Tuesday",
                "C) Wednesday",
                "D) Thursday"
            ],
            "answer": "B) Tuesday",
            "explanation": "Calculate elapsed days from 15th March to 15th August:\n• Remaining in March: $31 - 15 = 16\\text{ days} \\equiv 2\\pmod 7$\n• April: $30\\text{ days} \\equiv 2\\pmod 7$\n• May: $31\\text{ days} \\equiv 3\\pmod 7$\n• June: $30\\text{ days} \\equiv 2\\pmod 7$\n• July: $31\\text{ days} \\equiv 3\\pmod 7$\n• August: $15\\text{ days} \\equiv 1\\pmod 7$\n\nTotal odd days = $2 + 2 + 3 + 2 + 3 + 1 = 13 \\equiv 6\\text{ odd days}$.\n• Wednesday + 6 days = **Tuesday**."
        },
        {
            "id": 18,
            "category": "SSB OIR • Calendar (Leap Year Century Trick)",
            "question": "Cadet Vikram was born on **29th February 1896**. How many actual birthdays did he celebrate up to and including **29th February 1904**?",
            "visual": "Formula / Hint: In Gregorian calendar, century years are leap only if divisible by 400. Was 1900 a leap year?",
            "options": [
                "A) 2",
                "B) 4",
                "C) 1",
                "D) 0"
            ],
            "answer": "C) 1",
            "explanation": "• Cadet Vikram was born on a leap day: 29th February 1896.\n• The next 4th year was **1900**.\n• In the Gregorian calendar, a century year is a leap year **only if it is divisible by 400**. Since 1900 is NOT divisible by 400, the year 1900 was an ordinary year with only 28 days in February!\n• Thus, there was no 29th February in 1900.\n• The first leap day after his birth occurred on **29th February 1904**.\n• Therefore, by 29th February 1904, he had celebrated only **1** birthday."
        },
        {
            "id": 19,
            "category": "SSB OIR • Calendar (Maximum Leap Year Interval)",
            "question": "What is the **maximum possible gap** in years between two consecutive leap years in the calendar?",
            "visual": "Example: 1896 (Leap) to 1904 (Leap)  -->  Gap = 8 years (1900 skipped)",
            "options": [
                "A) 4 years",
                "B) 6 years",
                "C) 8 years",
                "D) 10 years"
            ],
            "answer": "C) 8 years",
            "explanation": "Leap years normally occur every 4 years. However, when a century year is not divisible by 400 (such as 1700, 1800, 1900, 2100), it is not a leap year.\n• For instance, between the leap year 1896 and the next leap year 1904, the intervening year 1900 is an ordinary year.\n• The gap between 1896 and 1904 is $1904 - 1896 = 8\\text{ years}$.\n\nHence, the maximum gap between two successive leap years is **8 years**."
        },
        {
            "id": 20,
            "category": "SSB OIR • Calendar (Constitution Day of India)",
            "question": "The Republic of India came into being with the adoption of its Constitution on **26th January 1950**. On which day of the week did 26th January 1950 fall?",
            "visual": "Formula / Hint: 1600 yrs = 0 odd days | 300 yrs = 1 odd day | 49 completed years (12 leap + 37 ord) + 26 days of Jan 1950",
            "options": [
                "A) Tuesday",
                "B) Wednesday",
                "C) Friday",
                "D) Thursday"
            ],
            "answer": "D) Thursday",
            "explanation": "Step-by-step Odd Days Calculation:\n1. 1600 years: 0 odd days.\n2. 300 years (1601–1900): 1 odd day.\n3. 49 completed years (1901–1949):\n• Leap years = $49 // 4 = 12$.\n• Ordinary years = $49 - 12 = 37$.\n• Total days = $(12 \\times 2) + (37 \\times 1) = 24 + 37 = 61\\text{ days} \\equiv 5\\text{ odd days } (61 \\pmod 7)$.\n\n4. Days in 1950 (up to 26 Jan):\n• 26 days $\\equiv 5\\text{ odd days } (26 \\pmod 7)$.\n\n5. Total odd days = $1 + 5 + 5 = 11 \\equiv 4\\text{ odd days } (11 \\pmod 7)$.\n• Day code 4 corresponds to **Thursday** (0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu).\n\nTherefore, 26th January 1950 was a **Thursday**."
        }
    ]


def get_question_bank(topic="Clocks & Calendar (SSB NAOO Entry PYQs • 20 Questions)"):
    """
    Returns the designated question bank.
    Defaults to the authentic 20 Previous Year Questions from Clocks & Calendar (SSB NAOO Entry).
    """
    if topic and ("Clocks" in topic or "Calendar" in topic):
        return get_clocks_and_calendar_pyq_bank()
    elif topic and "Coding" in topic:
        return get_coding_decoding_pyq_bank()
    return get_mixed_oir_bank()


# ==============================================================================
# 6. MODULAR HELPER FUNCTIONS & STATE MANAGEMENT
# ==============================================================================
def initialize_session_state():
    """Initializes and sanitizes Streamlit session state variables."""
    if "topic_mode" not in st.session_state:
        st.session_state.topic_mode = "Clocks & Calendar (SSB NAOO Entry PYQs • 20 Questions)"
    if "questions" not in st.session_state:
        st.session_state.questions = get_question_bank(st.session_state.topic_mode)
    if "current_q_idx" not in st.session_state:
        st.session_state.current_q_idx = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    if "max_streak" not in st.session_state:
        st.session_state.max_streak = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
    if "feedback_message" not in st.session_state:
        st.session_state.feedback_message = ""
    if "is_correct" not in st.session_state:
        st.session_state.is_correct = False
    if "sound_played" not in st.session_state:
        st.session_state.sound_played = False
    if "sound_enabled" not in st.session_state:
        st.session_state.sound_enabled = True
    if "show_hints" not in st.session_state:
        st.session_state.show_hints = True
    if "history" not in st.session_state:
        st.session_state.history = []
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False


def reset_quiz():
    """Resets the assessment state to start fresh."""
    st.session_state.current_q_idx = 0
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.max_streak = 0
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.feedback_message = ""
    st.session_state.is_correct = False
    st.session_state.sound_played = False
    st.session_state.history = []
    st.session_state.quiz_completed = False


def evaluate_user_answer(selected, correct_answer):
    """
    Evaluates candidate choice, updates streaks, and returns:
    (is_correct: bool, feedback_string: str)
    """
    is_correct = (selected == correct_answer)

    if is_correct:
        st.session_state.streak += 1
        if st.session_state.streak > st.session_state.max_streak:
            st.session_state.max_streak = st.session_state.streak
        phrase = random.choice(CORRECT_FEEDBACK_POOL)

        # Gamified milestone toast notifications
        if st.session_state.streak >= 5:
            st.toast("🌟 5 in a row! You're on an incredible streak!", icon="🔥")
        elif st.session_state.streak >= 3:
            st.toast("🔥 3 consecutive correct answers! Keep it going!", icon="✨")
        elif len(st.session_state.history) == 0:
            st.toast("🎉 First question correct! Off to a great start!", icon="🍫")

    else:
        st.session_state.streak = 0
        phrase = random.choice(INCORRECT_FEEDBACK_POOL)

    # Halfway toast
    if st.session_state.current_q_idx == 9:
        st.toast("🧭 Halfway milestone reached! 10 questions remaining.", icon="🎯")

    return is_correct, phrase


# ==============================================================================
# 7. UI COMPONENTS & RENDERING
# ==============================================================================
def render_header():
    """Renders the top VAISE header."""
    topic_label = st.session_state.get("topic_mode", "Clocks & Calendar (SSB NAOO Entry PYQs • 20 Questions)")
    st.markdown(f"""
    <div class="header-card">
        <span class="header-badge">VAISE • INTELLIGENCE & REASONING EVALUATION</span>
        <h1 class="header-title">VAISE</h1>
        <p class="header-subtitle">Interactive Assessment • {topic_label}</p>
    </div>
    """, unsafe_allow_html=True)


def render_question_grid():
    """Renders a tight, uniform 5x4 CSS grid of question indicators."""
    total_q = len(st.session_state.questions)
    grid_html = ['<div class="waypoint-grid">']
    for i in range(total_q):
        q_num = f"{i+1:02d}"
        if i < len(st.session_state.history):
            hist = st.session_state.history[i]
            if hist["is_correct"]:
                grid_html.append(f'<div class="wp-box wp-correct" title="Question {i+1}: Correct">✓ {q_num}</div>')
            else:
                grid_html.append(f'<div class="wp-box wp-wrong" title="Question {i+1}: Incorrect">✗ {q_num}</div>')
        elif i == st.session_state.current_q_idx and not st.session_state.quiz_completed:
            grid_html.append(f'<div class="wp-box wp-current" title="Question {i+1}: Current">📍 {q_num}</div>')
        else:
            grid_html.append(f'<div class="wp-box wp-pending" title="Question {i+1}: Upcoming">{q_num}</div>')
    grid_html.append('</div>')
    st.markdown("".join(grid_html), unsafe_allow_html=True)


def render_sidebar():
    """Renders the clean, high-contrast sidebar with stats and question matrix."""
    with st.sidebar:
        st.markdown("### 📊 Assessment Overview")
        st.markdown("**Platform:** VAISE")
        st.markdown("**Test Type:** Intelligence & Reasoning (OIR)")
        
        # Topic Module Selector
        topic_options = [
            "Clocks & Calendar (SSB NAOO Entry PYQs • 20 Questions)",
            "Coding & Decoding (Mandatory Topic • 20 PYQs)",
            "Comprehensive Mixed Assessment (20 Questions)"
        ]
        curr_mode = st.session_state.get("topic_mode", topic_options[0])
        if "Clocks" in curr_mode or "Calendar" in curr_mode:
            curr_idx = 0
        elif "Coding" in curr_mode:
            curr_idx = 1
        else:
            curr_idx = 2

        selected_mode = st.selectbox(
            "📚 Question Bank Topic",
            options=topic_options,
            index=curr_idx,
            key="topic_mode_select"
        )
        if selected_mode != st.session_state.get("topic_mode"):
            st.session_state.topic_mode = selected_mode
            st.session_state.questions = get_question_bank(selected_mode)
            reset_quiz()
            st.rerun()

        st.divider()

        # Sound Effects Toggle
        sound_on = st.toggle("🔊 Sound Effects (Hooray / Ohh)", value=st.session_state.sound_enabled)
        st.session_state.sound_enabled = sound_on

        hints_allowed = st.toggle("💡 Allow Formula / Hint Access", value=st.session_state.get("show_hints", True), help="Enables a collapsible 'Need a Formula / Hint?' box on questions.")
        st.session_state.show_hints = hints_allowed

        st.divider()

        # Score & Progress Tracking
        total_q = len(st.session_state.questions)
        curr = st.session_state.current_q_idx + 1 if not st.session_state.quiz_completed else total_q
        
        st.markdown(f"**Progress:** Question **{curr}** of **{total_q}**")
        progress = min(1.0, (curr - 1 if not st.session_state.quiz_completed else total_q) / total_q)
        st.progress(progress)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Score", f"{st.session_state.score} / {total_q}")
        with col2:
            acc = int((st.session_state.score / max(1, len(st.session_state.history))) * 100) if st.session_state.history else 0
            st.metric("Accuracy", f"{acc}%")

        # Streak Telemetry
        st.markdown(f"""
        <div style="background:#070d18; border:1px solid #1e3a8a; border-radius:8px; padding:10px; margin-top:8px; display:flex; justify-content:space-around; font-family:monospace;">
            <div>CURRENT STREAK: <strong style="color:#f59e0b;">🔥 {st.session_state.streak}X</strong></div>
            <div>BEST STREAK: <strong style="color:#38bdf8;">⭐ {st.session_state.max_streak}X</strong></div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Uniform 5x4 Question Status Grid
        st.markdown("#### 🎯 Question Tracker (20 Questions)")
        render_question_grid()

        st.divider()
        st.markdown("### 💡 Quick Tip")
        st.info("Read each question carefully. Focus on patterns, arithmetic consistency, and spatial symmetry.")

        if st.button("🔄 Restart Quiz", use_container_width=True):
            reset_quiz()
            st.rerun()


def render_quiz_screen():
    """Renders the single question interface with high-contrast options, sound effects, and chocolate shower."""
    q_idx = st.session_state.current_q_idx
    q_data = st.session_state.questions[q_idx]

    # Live HUD Stats Banner
    streak_label = f"🔥 {st.session_state.streak}X STREAK ACTIVE" if st.session_state.streak >= 2 else "✨ READY"
    st.markdown(f"""
    <div class="hud-banner">
        <div class="hud-stat"><span style="color:#38bdf8;">QUESTION:</span> {q_idx + 1:02d} / {len(st.session_state.questions)}</div>
        <div class="hud-stat streak-fire">{streak_label}</div>
        <div class="hud-stat"><span style="color:#10b981;">SCORE:</span> {st.session_state.score} PTS</div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    progress_val = q_idx / len(st.session_state.questions)
    st.progress(progress_val)

    # Main Question Box
    st.markdown(f"""
    <div class="question-box">
        <span class="category-tag">{q_data["category"]}</span>
        <div class="question-text">Q{q_idx + 1}. {q_data["question"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Visual / Diagram & Collapsible Formula/Hint
    visual = q_data.get("visual")
    if visual:
        # ASCII diagrams essential to read the problem (e.g., cube nets, matrices, dice positions)
        is_diagram = any(marker in visual for marker in ["+---+", "+--------+", "Position 1:"])
        if is_diagram:
            st.markdown(f'<div class="visual-container">{visual}</div>', unsafe_allow_html=True)
        elif st.session_state.get("show_hints", True):
            with st.expander("💡 Need a Formula / Hint? (Click to view)", expanded=False):
                st.markdown(f'<div class="visual-container" style="margin: 4px 0;">{visual}</div>', unsafe_allow_html=True)

    # Options Selection Area
    if not st.session_state.answered:
        selected = st.radio(
            "Select your answer:",
            q_data["options"],
            index=None,
            key=f"radio_q_{q_idx}"
        )

        col_left, col_submit, col_right = st.columns([1, 2, 1])
        with col_submit:
            submit_clicked = st.button("Submit Answer", type="primary", use_container_width=True)

        if submit_clicked:
            if selected is None:
                st.warning("⚠️ Please select an option before submitting your answer.")
            else:
                is_corr, phrase = evaluate_user_answer(selected, q_data["answer"])
                st.session_state.answered = True
                st.session_state.selected_option = selected
                st.session_state.is_correct = is_corr
                st.session_state.feedback_message = phrase
                st.session_state.sound_played = False  # Ready to play sound
                if is_corr:
                    st.session_state.score += 1
                
                # Append to history for summary review
                st.session_state.history.append({
                    "q_id": q_data["id"],
                    "question": q_data["question"],
                    "category": q_data["category"],
                    "user_choice": selected,
                    "correct_choice": q_data["answer"],
                    "is_correct": is_corr,
                    "feedback": phrase,
                    "explanation": q_data["explanation"]
                })
                st.rerun()

    else:
        # Trigger Sound Effects ("Hooray!" vs "Ohh!")
        if st.session_state.sound_enabled and not st.session_state.sound_played:
            play_sound_effect(st.session_state.is_correct)
            st.session_state.sound_played = True

        # Trigger the custom Chocolate Shower animation on correct answers!
        if st.session_state.is_correct:
            trigger_chocolate_shower()

        # Display Feedback Card
        if st.session_state.is_correct:
            st.markdown(f"""
            <div class="feedback-correct">
                <div class="feedback-phrase">{st.session_state.feedback_message}</div>
                <div class="feedback-detail"><strong>Your Answer:</strong> {st.session_state.selected_option} &nbsp;[CORRECT]</div>
                <div class="feedback-explanation"><strong>Explanation:</strong><br>{q_data['explanation']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feedback-incorrect">
                <div class="feedback-phrase">{st.session_state.feedback_message}</div>
                <div class="feedback-detail"><strong>Your Answer:</strong> {st.session_state.selected_option} ❌</div>
                <div class="feedback-detail"><strong>Correct Answer:</strong> {q_data['answer']} ✓</div>
                <div class="feedback-explanation"><strong>Explanation:</strong><br>{q_data['explanation']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Standard Next Button
        is_last = (q_idx == len(st.session_state.questions) - 1)
        next_label = "Finish & View Results 🏁" if is_last else "Next Question ➡️"

        col1, col_next, col2 = st.columns([1, 2, 1])
        with col_next:
            if st.button(next_label, type="primary", use_container_width=True):
                if is_last:
                    st.session_state.quiz_completed = True
                else:
                    st.session_state.current_q_idx += 1
                    st.session_state.answered = False
                    st.session_state.selected_option = None
                    st.session_state.feedback_message = ""
                    st.session_state.is_correct = False
                    st.session_state.sound_played = False
                st.rerun()


def render_summary_screen():
    """Renders the comprehensive score summary, sound, and celebration screen."""
    score = st.session_state.score
    total = len(st.session_state.questions)
    percentage = (score / total) * 100

    # Determine performance rating & sounds
    if score >= 18:
        tier_title = "🌟 OUTSTANDING • TIER 1"
        tier_color = "#10b981"
        summary_quote = "Exceptional analytical speed and reasoning! You operated with near-flawless accuracy across all verbal, spatial, and numerical patterns."
        trigger_chocolate_shower()
        if st.session_state.sound_enabled and not st.session_state.sound_played:
            play_sound_effect(True)
            st.session_state.sound_played = True
        st.balloons()
    elif score >= 15:
        tier_title = "⭐ EXCELLENT • TIER 2"
        tier_color = "#38bdf8"
        summary_quote = "Strong reasoning aptitude! You demonstrated high speed and precision across most challenging questions."
        trigger_chocolate_shower()
        if st.session_state.sound_enabled and not st.session_state.sound_played:
            play_sound_effect(True)
            st.session_state.sound_played = True
        st.balloons()
    elif score >= 12:
        tier_title = "⚡ ABOVE AVERAGE • TIER 3"
        tier_color = "#f59e0b"
        summary_quote = "Solid foundation! Fine-tune your speed on spatial cube nets and progressive number series to push into Tier 1."
        st.snow()
    elif score >= 9:
        tier_title = "🛡️ AVERAGE • TIER 4"
        tier_color = "#fb923c"
        summary_quote = "Good baseline performance! Review the detailed solutions below and retake the quiz to boost your score."
    else:
        tier_title = "💪 NEEDS IMPROVEMENT • TIER 5"
        tier_color = "#ef4444"
        summary_quote = "Practice makes perfect! Take your time to review every solution below, study the patterns, and try again."

    # Summary Hero Card
    st.markdown(f"""
    <div class="summary-card">
        <span class="header-badge">VAISE • ASSESSMENT REPORT</span>
        <h1 style="color: #ffffff !important; font-size: 2.2rem; margin: 10px 0;">{tier_title}</h1>
        <div style="display:inline-block; background:rgba(255,255,255,0.1); border:2px solid {tier_color}; border-radius:30px; padding:6px 22px; font-weight:900; font-size:1.1rem; color:#ffffff; margin:10px 0 16px 0;">
            FINAL SCORE: {score} / {total} ({percentage:.0f}%)
        </div>
        <p style="font-size: 0.98rem; color: #94a3b8; max-width: 620px; margin: 0 auto; line-height:1.5;">{summary_quote}</p>
    </div>
    """, unsafe_allow_html=True)

    # 4-Pill Key Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-pill">
            <div class="stat-num">{score}/{total}</div>
            <div class="stat-label">Total Score</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-pill">
            <div class="stat-num">{percentage:.0f}%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-pill">
            <div class="stat-num">{st.session_state.max_streak}X</div>
            <div class="stat-label">Best Streak</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="stat-pill">
            <div class="stat-num">{total}</div>
            <div class="stat-label">Questions</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Action Buttons
    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn1:
        if st.button("🔄 Restart Quiz", type="primary", use_container_width=True):
            reset_quiz()
            st.rerun()
    with c_btn2:
        if st.button("📋 Review Detailed Solutions Below", use_container_width=True):
            pass

    st.divider()

    # Detailed Question Review Accordion
    st.markdown("### 📋 Detailed Solutions (All 20 Questions)")
    st.caption("Inspect each question, your submitted response, and the complete logical explanation.")

    for idx, item in enumerate(st.session_state.history):
        status_icon = "🟢 CORRECT" if item["is_correct"] else "🔴 INCORRECT"
        header_text = f"Question {idx + 1:02d}: {item['category']} — {status_icon}"
        
        with st.expander(header_text, expanded=(not item["is_correct"])):
            st.markdown(f"**Question:**\n{item['question']}")
            
            c_ans1, c_ans2 = st.columns(2)
            with c_ans1:
                st.markdown(f"**Your Choice:** `{item['user_choice']}`")
            with c_ans2:
                st.markdown(f"**Correct Answer:** `{item['correct_choice']}`")

            st.markdown(f"**Explanation:**\n{item['explanation']}")


# ==============================================================================
# 8. MAIN APPLICATION ENTRYPOINT
# ==============================================================================
def main():
    """Main execution orchestrator."""
    initialize_session_state()
    render_header()
    render_sidebar()

    if not st.session_state.quiz_completed:
        render_quiz_screen()
    else:
        render_summary_screen()


if __name__ == "__main__":
    main()
