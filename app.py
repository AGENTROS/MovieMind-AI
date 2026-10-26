import html
import os
from datetime import date
import streamlit as st
import pandas as pd
import numpy as np
import requests

# Page configuration
st.set_page_config(
    page_title="MovieMind AI | Discover Beyond Limits",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Luxury Dark Palette matching Image (Dark: #060813, Sidebar: #0A0D1A, Card: #0E1424, Primary Accent: #2563EB, Cyan: #00D2FF)
st.markdown("""
<style>
    html, body, [class*="css"], .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: #060813 !important;
        color: #f1f5f9;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0a0d1a !important;
        border-right: 1px solid #141c2e !important;
    }
    [data-testid="stSidebar"] .stRadio > div {
        gap: 6px;
    }
    [data-testid="stSidebar"] .stRadio label {
        padding: 10px 14px;
        border-radius: 10px;
        transition: all 0.2s ease;
        color: #94a3b8 !important;
        font-weight: 500;
        cursor: pointer;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #111728 !important;
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] .stRadio [aria-checked="true"] {
        background: linear-gradient(90deg, #1d4ed8, #2563eb, #3b82f6) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.35) !important;
    }
    
    /* Top Header Bar */
    .top-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 0 20px 0;
        margin-bottom: 10px;
    }
    .header-search {
        flex-grow: 1;
        max-width: 680px;
        background: #0e1424;
        border: 1px solid #1c263e;
        border-radius: 10px;
        padding: 10px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #64748b;
    }
    .header-icons {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .icon-btn {
        background: #0e1424;
        border: 1px solid #1c263e;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        cursor: pointer;
        color: #94a3b8;
    }
    
    /* Hero Banner matching image */
    .hero-container {
        position: relative;
        width: 100%;
        min-height: 380px;
        border-radius: 18px;
        background: linear-gradient(90deg, rgba(6, 8, 19, 0.95) 0%, rgba(6, 8, 19, 0.75) 45%, rgba(6, 8, 19, 0.2) 100%),
                    url('https://image.tmdb.org/t/p/original/rAiYTsqJJq0AhHggLbgti95OXjM.jpg');
        background-size: cover;
        background-position: center right;
        border: 1px solid #172138;
        padding: 44px 40px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.7);
        margin-bottom: 24px;
        overflow: hidden;
    }
    .featured-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(6, 182, 212, 0.15);
        color: #22d3ee;
        border: 1px solid rgba(6, 182, 212, 0.35);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        width: fit-content;
        margin-bottom: 12px;
    }
    .hero-movie-title {
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 12px;
        letter-spacing: -0.8px;
    }
    .hero-movie-title .title-white {
        color: #ffffff;
    }
    .hero-movie-title .title-cyan {
        color: #00d2ff;
        background: linear-gradient(135deg, #38bdf8 0%, #00d2ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc {
        max-width: 540px;
        font-size: 0.96rem;
        line-height: 1.55;
        color: #94a3b8;
        margin-bottom: 14px;
    }
    .hero-meta {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.9rem;
        color: #cbd5e1;
        margin-bottom: 24px;
    }
    .hero-star {
        color: #facc15;
        font-weight: 700;
    }
    .hero-actions {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .btn-trailer {
        background: #2563eb;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.9rem;
        padding: 10px 22px;
        border-radius: 8px;
        border: none;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        text-decoration: none;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
        transition: transform 0.2s ease, background 0.2s ease;
    }
    .btn-trailer:hover {
        background: #1d4ed8;
        transform: translateY(-2px);
    }
    .btn-watchlist {
        background: rgba(255, 255, 255, 0.08);
        color: #f8fafc;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 10px 20px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.16);
        display: inline-flex;
        align-items: center;
        gap: 8px;
        backdrop-filter: blur(8px);
        text-decoration: none;
        transition: all 0.2s ease;
    }
    .btn-watchlist:hover {
        background: rgba(255, 255, 255, 0.15);
    }

    /* 4 Stat Cards Row */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 30px;
    }
    .stat-card-box {
        background: #0e1424;
        border: 1px solid #1a233a;
        border-radius: 14px;
        padding: 18px 20px;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .stat-card-box:hover {
        border-color: #2563eb;
        transform: translateY(-2px);
    }
    .stat-icon-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: rgba(37, 99, 235, 0.15);
        color: #38bdf8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.35rem;
        flex-shrink: 0;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    .stat-number {
        font-size: 1.55rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.2;
    }
    .stat-label-text {
        font-size: 0.8rem;
        color: #94a3b8;
    }

    /* Movie Cards Grid */
    .movie-thumb-card {
        background: #0e1424;
        border: 1px solid #1a233a;
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.25s ease;
        display: flex;
        flex-direction: column;
        height: 100%;
        position: relative;
    }
    .movie-thumb-card:hover {
        transform: translateY(-6px);
        border-color: #2563eb;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6), 0 0 16px rgba(37, 99, 235, 0.25);
    }
    .poster-wrap {
        position: relative;
        width: 100%;
        padding-top: 142%;
        overflow: hidden;
        background: #090d18;
    }
    .poster-wrap img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .heart-badge {
        position: absolute;
        top: 8px;
        right: 8px;
        background: rgba(10, 13, 26, 0.7);
        backdrop-filter: blur(6px);
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .card-info {
        padding: 10px 12px;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    .card-title {
        font-weight: 700;
        font-size: 0.88rem;
        color: #f8fafc;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 3px;
    }
    .card-sub {
        font-size: 0.78rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
    }
    .card-genres {
        display: flex;
        gap: 4px;
        flex-wrap: wrap;
    }
    .genre-chip {
        background: #151d30;
        color: #cbd5e1;
        font-size: 0.68rem;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid #1e2a44;
    }

    /* Popular Genres Themed Buttons */
    .genre-palette-grid {
        display: flex;
        gap: 10px;
        overflow-x: auto;
        padding-bottom: 10px;
        margin-bottom: 25px;
    }
    .genre-pill-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        white-space: nowrap;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-width: 1px;
        border-style: solid;
        text-decoration: none;
    }
    .genre-pill-btn:hover {
        transform: translateY(-2px);
    }
    .g-action { background: #1c0e12; border-color: #ef4444; color: #fca5a5; }
    .g-adv { background: #1c1308; border-color: #f59e0b; color: #fcd34d; }
    .g-scifi { background: #081726; border-color: #06b6d4; color: #67e8f9; }
    .g-drama { background: #160c24; border-color: #a855f7; color: #d8b4fe; }
    .g-comedy { background: #1a1708; border-color: #eab308; color: #fde047; }
    .g-thriller { background: #081a17; border-color: #14b8a6; color: #5eead4; }
    .g-horror { background: #1c0911; border-color: #f43f5e; color: #fda4af; }
    .g-romance { background: #1c0918; border-color: #ec4899; color: #f9a8d4; }
    .g-anim { background: #120e29; border-color: #8b5cf6; color: #c4b5fd; }
    .g-crime { background: #101624; border-color: #64748b; color: #cbd5e1; }

    /* Guest User Card in Sidebar */
    .guest-user-box {
        background: #0e1424;
        border: 1px solid #1a233a;
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .guest-btn {
        background: linear-gradient(90deg, #2563eb, #00d2ff);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 9px 14px;
        border-radius: 8px;
        border: none;
        width: 100%;
        text-align: center;
        display: block;
    }

    /* Netflix Horizontal Carousel Slider */
    .netflix-section {
        position: relative;
        margin-bottom: 35px;
    }
    .netflix-section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .netflix-section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    .netflix-slider-wrap {
        position: relative;
        width: 100%;
    }
    .netflix-slider-wrap:hover .netflix-nav-arrow {
        opacity: 1;
    }
    .netflix-slider-track {
        display: flex;
        gap: 16px;
        overflow-x: auto;
        scroll-behavior: smooth;
        padding: 16px 4px 22px 4px;
        scrollbar-width: thin;
        scrollbar-color: #2563eb #0e1424;
        -webkit-overflow-scrolling: touch;
    }
    .netflix-slider-track::-webkit-scrollbar {
        height: 6px;
    }
    .netflix-slider-track::-webkit-scrollbar-track {
        background: #090d18;
        border-radius: 4px;
    }
    .netflix-slider-track::-webkit-scrollbar-thumb {
        background: #2563eb;
        border-radius: 4px;
    }
    .netflix-nav-arrow {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: 44px;
        height: 120px;
        background: rgba(6, 8, 19, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #ffffff;
        font-size: 2.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 40;
        opacity: 0;
        transition: all 0.25s ease;
        backdrop-filter: blur(8px);
        border-radius: 8px;
    }
    .netflix-nav-arrow:hover {
        background: rgba(37, 99, 235, 0.9);
        color: #fff;
        transform: translateY(-50%) scale(1.06);
    }
    .arrow-prev { left: 0; }
    .arrow-next { right: 0; }
    
    /* Netflix Card Zoom Animation */
    .n-card {
        flex: 0 0 205px;
        background: #0e1424;
        border: 1px solid #1a233a;
        border-radius: 10px;
        overflow: hidden;
        cursor: pointer;
        transition: transform 0.35s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.35s ease, border-color 0.35s ease;
        position: relative;
    }
    .n-card:hover {
        transform: scale(1.09) translateY(-6px);
        z-index: 30;
        border-color: #3b82f6;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.85), 0 0 18px rgba(37, 99, 235, 0.35);
    }
    .n-poster-box {
        position: relative;
        width: 100%;
        padding-top: 142%;
        overflow: hidden;
        background: #090d18;
    }
    .n-poster-box img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .netflix-badge-red {
        position: absolute;
        bottom: 8px;
        left: 8px;
        background: #e50914;
        color: #ffffff;
        font-size: 0.65rem;
        font-weight: 800;
        padding: 3px 6px;
        border-radius: 3px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }

    /* Top 10 Giant Numbers */
    .top10-item-wrap {
        display: flex;
        align-items: flex-end;
        flex: 0 0 250px;
        position: relative;
        transition: transform 0.35s ease;
    }
    .top10-item-wrap:hover {
        transform: scale(1.08) translateY(-4px);
        z-index: 30;
    }
    .top10-huge-num {
        font-size: 7.6rem;
        font-weight: 900;
        line-height: 0.72;
        color: #060813;
        -webkit-text-stroke: 4px #596579;
        text-shadow: 0 0 12px rgba(0, 0, 0, 0.9);
        margin-right: -24px;
        z-index: 1;
        user-select: none;
    }
    .top10-card {
        width: 165px;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #1a233a;
        background: #0e1424;
        z-index: 2;
        box-shadow: 0 10px 25px rgba(0,0,0,0.7);
        position: relative;
    }
    .top10-poster {
        position: relative;
        width: 100%;
        padding-top: 142%;
        overflow: hidden;
        background: #090d18;
    }
    .top10-poster img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* =========================================================
       NIGHTPICKS & PICKAMOVIE & MOVIEDECIDER STYLES
       ========================================================= */
    .night-hero-box {
        text-align: center;
        padding: 24px 20px 10px 20px;
        max-width: 820px;
        margin: 0 auto;
    }
    .night-main-title {
        font-size: 3.4rem;
        font-weight: 900;
        letter-spacing: -1.2px;
        color: #ffffff;
        line-height: 1.1;
        margin-bottom: 12px;
    }
    .night-sub-text {
        font-size: 1.15rem;
        color: #94a3b8;
        line-height: 1.5;
        margin-bottom: 24px;
    }
    .night-preset-grid {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 24px;
    }
    .night-chip {
        background: #0e1424;
        border: 1px solid #1e2a44;
        color: #94a3b8;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 7px 16px;
        border-radius: 999px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .night-chip:hover {
        border-color: #3b82f6;
        color: #ffffff;
        background: #162038;
        transform: translateY(-2px);
    }
    
    .night-result-box {
        background: #0c101d;
        border: 1px solid #1a243d;
        border-radius: 20px;
        overflow: hidden;
        display: flex;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85);
        margin: 24px 0;
        position: relative;
    }
    .night-poster-col {
        flex: 0 0 310px;
        position: relative;
        background: #060813;
        overflow: hidden;
    }
    .night-poster-col img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }
    .night-info-col {
        padding: 34px 38px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        flex-grow: 1;
    }
    .night-res-title {
        font-size: 2.25rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
        line-height: 1.15;
    }
    .night-meta-row {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 0.95rem;
        color: #cbd5e1;
        margin-bottom: 14px;
        flex-wrap: wrap;
    }
    .night-meta-pill {
        background: #141b2d;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid #1f2a44;
        color: #94a3b8;
    }
    .night-trailer-btn {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: background 0.2s;
    }
    .night-trailer-btn:hover {
        background: rgba(255, 255, 255, 0.22);
    }
    .night-available-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.76rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 14px;
    }
    .night-platform-tag {
        background: #111827;
        border: 1px solid #23304a;
        color: #e2e8f0;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .night-res-overview {
        color: #94a3b8;
        font-size: 0.98rem;
        line-height: 1.6;
        margin-bottom: 22px;
    }

    .pickme-wrapper {
        background: rgba(14, 20, 36, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 14px;
        padding: 26px 30px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
        margin: 20px 0;
    }
    .pickme-btn-red {
        background: #e50914;
        color: #ffffff !important;
        font-weight: 800;
        font-size: 0.92rem;
        padding: 12px 24px;
        border-radius: 6px;
        border: none;
        text-align: center;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        text-decoration: none;
        box-shadow: 0 4px 16px rgba(229, 9, 20, 0.4);
        transition: transform 0.2s, background 0.2s;
    }
    .pickme-btn-red:hover {
        background: #c10711;
        transform: translateY(-2px);
    }
    .pickme-btn-outline {
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.35);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.92rem;
        padding: 12px 24px;
        border-radius: 6px;
        text-align: center;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    .pickme-btn-outline:hover {
        border-color: #ffffff;
        background: rgba(255, 255, 255, 0.08);
    }

    .decider-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin: 25px 0 35px 0;
    }
    .decider-box {
        background: #0e1424;
        border: 1px solid #1a233a;
        border-radius: 14px;
        padding: 22px;
        transition: all 0.25s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    .decider-box:hover {
        border-color: #3b82f6;
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
    }
    .decider-pill {
        background: rgba(37, 99, 235, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(37, 99, 235, 0.3);
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        width: fit-content;
        margin-bottom: 10px;
    }
    .decider-title {
        font-size: 1.18rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
        line-height: 1.25;
    }
    .decider-desc {
        font-size: 0.86rem;
        color: #94a3b8;
        line-height: 1.5;
        margin-bottom: 16px;
        flex-grow: 1;
    }
    .decider-editorial-banner {
        background: #0a0d1a;
        border-left: 3px solid #00d2ff;
        padding: 20px 24px;
        border-radius: 0 12px 12px 0;
        margin: 16px 0 24px 0;
        font-size: 0.98rem;
        color: #cbd5e1;
        line-height: 1.65;
    }

    .night-steps-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 35px 0 25px 0;
    }
    .night-step-card {
        border-left: 2px solid #2563eb;
        padding-left: 14px;
    }
    .night-step-num {
        font-size: 1.8rem;
        font-weight: 900;
        color: #3b82f6;
        line-height: 1;
        margin-bottom: 4px;
    }
    .night-step-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .night-step-desc {
        font-size: 0.82rem;
        color: #94a3b8;
        line-height: 1.45;
    }

    .category-cards-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin: 16px 0 30px 0;
    }
    .cat-card-item {
        background: #0e1424;
        border: 1px solid #1a233a;
        border-radius: 12px;
        padding: 16px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        transition: transform 0.2s, border-color 0.2s;
    }
    .cat-card-item:hover {
        transform: translateY(-2px);
        border-color: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# Imports of project modules
from data_loader import get_processed_data
from content_based import ContentBasedRecommender
from collaborative import CollaborativeRecommender
from hybrid import HybridRecommender
from tmdb_api import tmdb_client
from movie_filters import filter_movies
from movie_sources import omdb_client, save_env_value
from evaluation import get_cached_or_default_metrics
from curated_lists import CURATED_LISTS, QUIZ_MOODS, QUIZ_OCCASIONS, QUIZ_SPECIAL_THEMES, QUIZ_ERAS

# Initialize Data & Models with caching
@st.cache_resource(show_spinner="Initializing Recommendation Engine...")
def initialize_system():
    movies_df, ratings_df = get_processed_data()
    cb_model = ContentBasedRecommender(movies_df)
    cf_model = CollaborativeRecommender(movies_df, ratings_df)
    hybrid_model = HybridRecommender(cb_model, cf_model)
    return movies_df, ratings_df, cb_model, cf_model, hybrid_model


@st.cache_data(ttl=3600, show_spinner=False)
def get_live_movie_page(
    sort_by, release_date_gte=None, release_date_lte=None, minimum_votes=0
):
    filters = {"vote_count.gte": minimum_votes}
    if release_date_gte:
        filters["primary_release_date.gte"] = release_date_gte
    if release_date_lte:
        filters["primary_release_date.lte"] = release_date_lte
    return tmdb_client.discover_movies(page=1, sort_by=sort_by, filters=filters)["results"]


def get_movie_metadata(tmdb_id, title, year, refresh=False):
    details = tmdb_client.get_movie_details(
        tmdb_id=tmdb_id, title=title, year=year, refresh=refresh
    )
    if omdb_client.api_key:
        try:
            omdb_details = omdb_client.get_movie_details(
                imdb_id=details.get("imdb_id"), title=title, year=year
            )
        except requests.RequestException as error:
            st.warning(f"OMDb details could not be loaded: {error}")
            omdb_details = None
        if omdb_details:
            details["imdb_id"] = omdb_details.get(
                "imdbID", details.get("imdb_id")
            )
            details["runtime"] = (
                omdb_details.get("runtime_minutes") or details.get("runtime")
            )
            details["overview"] = omdb_details.get("Plot") or details.get("overview")
            details["poster_path"] = (
                omdb_details.get("Poster")
                if omdb_details.get("Poster") not in {None, "N/A"}
                else details.get("poster_path")
            )
            details["genres"] = [
                genre.strip()
                for genre in omdb_details.get("Genre", "").split(",")
                if genre.strip()
            ] or details.get("genres", [])
            details["imdb_rating"] = omdb_details.get("imdbRating")
            details["imdb_votes"] = omdb_details.get("imdbVotes")
            details["actors"] = omdb_details.get("Actors")
            details["director"] = omdb_details.get("Director")
            details["awards"] = omdb_details.get("Awards")
            details["language"] = omdb_details.get("Language")
            details["country"] = omdb_details.get("Country")
            details["released"] = omdb_details.get("Released")
    return details


def normalize_tmdb_movie(item):
    genre_names = {
        12: "Adventure", 14: "Fantasy", 16: "Animation", 18: "Drama",
        27: "Horror", 28: "Action", 35: "Comedy", 37: "Western",
        53: "Thriller", 80: "Crime", 99: "Documentary", 878: "Sci-Fi",
        9648: "Mystery", 10749: "Romance", 10751: "Family",
        10752: "War", 10770: "TV Movie",
    }
    title = item.get("title") or item.get("original_title") or "Untitled"
    release_date = item.get("release_date", "")
    year = int(release_date[:4]) if len(release_date) >= 4 else None
    tmdb_id = int(item["id"])
    genres = [genre_names[g] for g in item.get("genre_ids", []) if g in genre_names]
    return {
        "movieId": 1_000_000_000 + tmdb_id,
        "title": f"{title} ({year})" if year else title,
        "clean_title": title,
        "year": year,
        "genres": "|".join(genres),
        "genres_str": ", ".join(genres),
        "avg_rating": float(item.get("vote_average") or 0) / 2,
        "rating_count": int(item.get("vote_count") or 0),
        "tmdbId": tmdb_id,
        "imdbId": "",
        "is_external": True,
    }


movies_df, ratings_df, cb_model, cf_model, hybrid_model = initialize_system()

# Session State for User Ratings & Navigation
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = {
        79132: 5.0,  # Inception
        109487: 5.0, # Interstellar
        58559: 4.5   # The Dark Knight
    }
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'selected_movie_id' not in st.session_state:
    st.session_state.selected_movie_id = 109487 # Interstellar default
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Home"
if 'night_current_pick' not in st.session_state:
    st.session_state.night_current_pick = None
if 'night_history' not in st.session_state:
    st.session_state.night_history = []
if 'quiz_candidates' not in st.session_state:
    st.session_state.quiz_candidates = []
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
if 'selected_curated_list' not in st.session_state:
    st.session_state.selected_curated_list = None
if 'home_recommendations' not in st.session_state:
    st.session_state.home_recommendations = None
if 'home_recommendation_signature' not in st.session_state:
    st.session_state.home_recommendation_signature = None
if 'selected_remote_movie' not in st.session_state:
    st.session_state.selected_remote_movie = None

# Helper to sample a movie for NightPicks Random Generator
def sample_night_pick(
    mood=None, era=None, min_rating=0.0, preset=None, sort_by=None,
    streaming_provider=None,
):
    df = movies_df.copy()
    
    # Save active filter state in session so "Spin Again" respects same filters
    st.session_state.night_active_mood = mood
    st.session_state.night_active_era = era
    st.session_state.night_active_min_rat = min_rating
    st.session_state.night_active_preset = preset
    st.session_state.night_active_sort = sort_by
    st.session_state.night_active_provider = streaming_provider
    
    if tmdb_client.api_key or tmdb_client.read_token:
        genre_ids = {
            "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35,
            "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751,
            "Fantasy": 14, "Horror": 27, "Mystery": 9648, "Romance": 10749,
            "Sci-Fi": 878, "Thriller": 53, "War": 10752, "Western": 37,
        }
        filters = {"vote_count.gte": 20, "include_adult": False}
        tmdb_sort = {
            "Top Rated": "vote_average.desc",
            "Newest": "primary_release_date.desc",
        }.get(sort_by, "popularity.desc")
        if mood in genre_ids:
            filters["with_genres"] = genre_ids[mood]
        if era in {"70s", "80s", "90s", "00s", "10s", "20s"}:
            decade = {"70s": 1970, "80s": 1980, "90s": 1990, "00s": 2000,
                      "10s": 2010, "20s": 2020}[era]
            filters["primary_release_date.gte"] = f"{decade}-01-01"
            end_year = min(decade + 9, date.today().year)
            filters["primary_release_date.lte"] = f"{end_year}-12-31"
        providers = {
            "Netflix": 8,
            "Prime Video": 119,
            "Disney+ Hotstar": 122,
            "Apple TV+": 350,
        }
        if streaming_provider in providers:
            filters.update({
                "with_watch_providers": providers[streaming_provider],
                "watch_region": "IN",
                "with_watch_monetization_types": "flatrate",
            })
        if min_rating > 0:
            filters["vote_average.gte"] = min_rating
        if preset == "under_90":
            filters["with_runtime.lte"] = 89
        elif preset == "hidden_gem":
            filters.update({
                "vote_average.gte": max(filters.get("vote_average.gte", 0), 7.0),
                "vote_count.lte": 1000,
            })
            tmdb_sort = "vote_average.desc"
        elif preset == "date_night":
            date_genres = "35|10749|18"
            if filters.get("with_genres"):
                date_genres = f"{filters['with_genres']},{date_genres}"
            filters.update({
                "with_genres": date_genres,
                "vote_average.gte": max(filters.get("vote_average.gte", 0), 6.6),
            })
        elif preset == "highly_rated":
            filters["vote_average.gte"] = max(filters.get("vote_average.gte", 0), 7.6)

        try:
            first_page = tmdb_client.discover_movies(
                page=1, sort_by=tmdb_sort, filters=filters
            )
            max_page = min(int(first_page.get("total_pages", 1)), 500)
            chosen_page = np.random.randint(1, max_page + 1)
            page_data = (
                first_page if chosen_page == 1
                else tmdb_client.discover_movies(
                    page=chosen_page, sort_by=tmdb_sort, filters=filters
                )
            )
            candidates = page_data["results"]
            np.random.shuffle(candidates)
            for candidate in candidates:
                tmdb_id = int(candidate["id"])
                title = candidate.get("title") or candidate.get("original_title")
                release_date = candidate.get("release_date", "")
                year = int(release_date[:4]) if len(release_date) >= 4 else None
                existing = movies_df[movies_df["tmdbId"] == tmdb_id]
                movie_id = (
                    int(existing.iloc[0]["movieId"])
                    if not existing.empty
                    else 1_000_000_000 + tmdb_id
                )
                if movie_id in st.session_state.get("night_history", []):
                    continue
                if not existing.empty:
                    movie = existing.iloc[0].to_dict()
                else:
                    movie = {
                        "movieId": movie_id,
                        "title": f"{title} ({year})" if year else title,
                        "clean_title": title,
                        "year": year,
                        "genres": "",
                        "genres_str": "",
                        "avg_rating": float(candidate.get("vote_average") or 0) / 2,
                        "rating_count": int(candidate.get("vote_count") or 0),
                        "tmdbId": tmdb_id,
                        "imdbId": "",
                    }
                movie["tmdbId"] = tmdb_id
                movie["is_external"] = existing.empty
                movie["watch_provider"] = streaming_provider
                if preset == "under_90":
                    details = get_movie_metadata(tmdb_id, title, year)
                    runtime = details.get("runtime")
                    if runtime is None or int(runtime) >= 90:
                        continue
                    movie["runtime"] = int(runtime)
                st.session_state.selected_remote_movie = movie if existing.empty else None
                break
            else:
                st.session_state.night_picker_error = (
                    "No movie matched all selected filters with verified runtime. "
                    "Try changing the filters and spin again."
                )
                return None
        except RuntimeError as error:
            st.session_state.night_picker_error = str(error)
            return None
        else:
            st.session_state.night_picker_error = None
            sampled_row = movie
    else:
        if preset == "under_90" and "runtime" not in df.columns:
            st.session_state.night_picker_error = (
                "Verified runtime data is needed for the Under-90 filter. "
                "Configure a TMDB key in Settings; OMDb cannot discover titles."
            )
            return None
        if streaming_provider:
            st.session_state.night_picker_error = (
                "Streaming availability requires a live TMDB connection."
            )
            return None
        filtered = filter_movies(
            df,
            mood=mood,
            era=era,
            min_rating=min_rating,
            preset=preset,
            excluded_ids=st.session_state.get("night_history", []),
        )
        if filtered.empty and st.session_state.get("night_history"):
            st.session_state.night_history = []
            filtered = filter_movies(
                df, mood=mood, era=era, min_rating=min_rating, preset=preset
            )
        if filtered.empty:
            st.session_state.night_picker_error = (
                "No movie matched all selected filters. Try changing the filters."
            )
            return None
        quality_pool = filtered[filtered["rating_count"] >= 3]
        if len(quality_pool) >= 15:
            filtered = quality_pool
        if sort_by == "Top Rated":
            filtered = filtered.sort_values(
                ["avg_rating", "rating_count"], ascending=[False, False]
            ).head(50)
        elif sort_by == "Newest":
            filtered = filtered.sort_values(
                ["year", "rating_count"], ascending=[False, False]
            ).head(50)
        else:
            filtered = filtered.sort_values(
                ["rating_count", "avg_rating"], ascending=[False, False]
            ).head(50)
        sampled_row = filtered.sample(1).iloc[0].to_dict()
        st.session_state.night_picker_error = None

    mid = int(sampled_row['movieId'])
    if 'night_history' not in st.session_state:
        st.session_state.night_history = []
    if mid not in st.session_state.night_history:
        st.session_state.night_history.append(mid)
        if len(st.session_state.night_history) > 100:
            st.session_state.night_history.pop(0)
            
    return sampled_row

# Helper to resolve a curated list movie into rich metadata
def resolve_curated_movie(item):
    title = item.get('title', '')
    year = item.get('year')
    match = movies_df[movies_df['clean_title'].str.lower() == title.lower()]
    if match.empty:
        match = movies_df[movies_df['title'].str.lower().str.contains(title.lower(), regex=False)]
    
    if not match.empty:
        row = match.iloc[0].to_dict()
        row['avg_rating'] = item.get('rating', row.get('avg_rating', 8.0))
        return row
    else:
        return {
            'movieId': abs(hash(title)) % 1000000,
            'title': f"{title} ({year})" if year else title,
            'clean_title': title,
            'year': year or 2020,
            'avg_rating': item.get('rating', 8.0),
            'genres_str': item.get('genres', 'Drama, Thriller'),
            'rating_count': 1200,
            'tmdbId': 0
        }

# Modern Card Renderer matching Image 1:1
def render_movie_card(movie_row, score_badge=None, col_obj=None, card_key=None):
    mid = int(movie_row['movieId'])
    title = str(movie_row.get('clean_title', movie_row.get('title', 'Movie')))
    safe_title = html.escape(title)
    raw_year = movie_row.get('year')
    year_str = str(int(raw_year)) if raw_year and not pd.isna(raw_year) else "2024"
    
    genres = movie_row.get('genres_str', '')
    g_chips = "".join([f"<span class='genre-chip'>{g.strip()}</span>" for g in genres.split(',')[:2]])
    rating = movie_row.get('avg_rating', 0.0)
    tmdb_id = int(movie_row.get('tmdbId', 0))

    details = tmdb_client.get_movie_details(tmdb_id=tmdb_id, title=title, year=raw_year)
    poster_url = html.escape(str(details.get('poster_path') or ""), quote=True)

    target = col_obj if col_obj is not None else st

    with target:
        badge_html = f"<span style='color:#34d399; font-weight:700; font-size:0.75rem;'>• {score_badge}</span>" if score_badge else ""
        card_html = (
            f"<div class='movie-thumb-card'>"
            f"<div class='poster-wrap'>"
            f"<img src='{poster_url}' alt='{safe_title}' loading='lazy' />"
            f"<div class='heart-badge'>♡</div>"
            f"</div>"
            f"<div class='card-info'>"
            f"<div class='card-title' title='{safe_title}'>{safe_title}</div>"
            f"<div class='card-sub'>"
            f"<span>{year_str}</span>"
            f"<span style='color:#facc15; font-weight:700;'>★ {rating:.1f}</span>"
            f"{badge_html}"
            f"</div>"
            f"<div class='card-genres'>{g_chips}</div>"
            f"</div>"
            f"</div>"
        )
        st.markdown(card_html, unsafe_allow_html=True)
        btn_key = card_key if card_key else f"btn_{mid}_{abs(hash(str(mid) + str(target))) % 10000000}"
        if st.button("Details", key=btn_key, use_container_width=True):
            st.session_state.selected_movie_id = mid
            st.session_state.selected_remote_movie = (
                movie_row if movie_row.get("is_external") else None
            )
            st.session_state.active_tab = "Movie Details"
            st.rerun()

def render_night_result_card(movie_row):
    mid = int(movie_row.get('movieId', 0))
    title = str(movie_row.get('clean_title', movie_row.get('title', 'Movie')))
    raw_year = movie_row.get('year', 2024)
    year_str = str(int(raw_year)) if raw_year and not pd.isna(raw_year) else "2024"
    rating = float(movie_row.get('avg_rating', 7.8))
    tmdb_id = int(movie_row.get('tmdbId', 0))
    
    details = get_movie_metadata(tmdb_id, title, raw_year)
    safe_title = html.escape(title)
    poster_url = html.escape(str(details.get('poster_path') or ""), quote=True)
    overview = html.escape(
        str(details.get('overview') or "No overview available for this title.")
    )
    trailer_url = html.escape(
        str(details.get('trailer_url') or "https://www.youtube.com"), quote=True
    )
    runtime = movie_row.get("runtime") or details.get("runtime")
    runtime_str = f"{int(runtime)}M" if runtime else "Runtime unavailable"
    tmdb_rating = details.get('vote_average', rating)
    
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown(
            f"<div style='border-radius:14px; overflow:hidden; box-shadow:0 12px 30px rgba(0,0,0,0.8); background:#060813;'>"
            f"<img src='{poster_url}' style='width:100%; display:block;' />"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_r:
        st.markdown(
            f"<h2 style='font-size:2.4rem; font-weight:800; color:#fff; margin:0 0 10px 0;'>{safe_title}</h2>"
            f"<div style='display:flex; align-items:center; gap:12px; margin-bottom:14px; flex-wrap:wrap;'>"
            f"<span style='background:#141b2d; border:1px solid #1f2a44; color:#94a3b8; padding:3px 10px; border-radius:6px; font-weight:600;'>📅 {year_str}</span>"
            f"<span style='background:#141b2d; border:1px solid #1f2a44; color:#94a3b8; padding:3px 10px; border-radius:6px; font-weight:600;'>⏱ {runtime_str}</span>"
            f"<span style='background:#1e3a8a; color:#60a5fa; padding:3px 10px; border-radius:6px; font-weight:700;'>★ {tmdb_rating:.1f}</span>"
            f"<a href='{trailer_url}' target='_blank' class='night-trailer-btn'>▶ &nbsp; Watch Trailer</a>"
            f"</div>"
            f"<div class='night-available-bar'>"
            f"{'AVAILABLE ON: ' + html.escape(movie_row['watch_provider']) + ' (India)' if movie_row.get('watch_provider') else 'STREAMING AVAILABILITY NOT CHECKED'}"
            f"</div>"
            f"<div style='color:#cbd5e1; font-size:1rem; line-height:1.65; margin-bottom:20px;'>{overview}</div>",
            unsafe_allow_html=True
        )
        
        btn_c1, btn_c2, btn_c3 = st.columns([1.5, 1.5, 1])
        with btn_c1:
            if st.button("▶ Watch Now / Details", key="night_btn_details", use_container_width=True):
                st.session_state.selected_movie_id = mid
                st.session_state.selected_remote_movie = (
                    movie_row if movie_row.get("is_external") else None
                )
                st.session_state.active_tab = "Movie Details"
                st.rerun()
        with btn_c2:
            if st.button("🔄 Spin Again", key="night_btn_spin", use_container_width=True):
                st.session_state.night_current_pick = sample_night_pick(
                    mood=st.session_state.get('night_active_mood'),
                    era=st.session_state.get('night_active_era'),
                    min_rating=st.session_state.get('night_active_min_rat', 0.0),
                    preset=st.session_state.get('night_active_preset'),
                    sort_by=st.session_state.get("night_active_sort"),
                    streaming_provider=st.session_state.get("night_active_provider"),
                )
                st.session_state.night_pick_requested = True
                st.rerun()
        with btn_c3:
            if st.button("🔖 + Watchlist", key="night_btn_wl", use_container_width=True):
                if title not in st.session_state.watchlist:
                    st.session_state.watchlist.append(title)
                    st.toast(f"Added {title} to Watchlist!", icon="🔖")

def render_pickme_result_card(movie_row, candidates=None, current_idx=0):
    mid = int(movie_row.get('movieId', 0))
    title = str(movie_row.get('clean_title', movie_row.get('title', 'Movie')))
    raw_year = movie_row.get('year', 2024)
    year_str = str(int(raw_year)) if raw_year and not pd.isna(raw_year) else "2024"
    rating = float(movie_row.get('avg_rating', 7.8))
    genres = movie_row.get('genres_str', 'Drama, Thriller')
    tmdb_id = int(movie_row.get('tmdbId', 0))
    
    details = tmdb_client.get_movie_details(tmdb_id=tmdb_id, title=title, year=raw_year)
    poster_url = details.get('poster_path')
    overview = details.get('overview', "No overview available for this title.")
    trailer_url = details.get('trailer_url', 'https://www.youtube.com')
    
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:700; margin-bottom:14px;'>Recommended for you:</h3>", unsafe_allow_html=True)
    
    pm_col1, pm_col2 = st.columns([1, 2.5])
    with pm_col1:
        st.markdown(
            f"<div style='border-radius:10px; overflow:hidden; border:1px solid #1a233a; background:#060813; box-shadow:0 10px 25px rgba(0,0,0,0.7);'>"
            f"<img src='{poster_url}' style='width:100%; display:block;' />"
            f"</div>",
            unsafe_allow_html=True
        )
    with pm_col2:
        st.markdown(
            f"<h2 style='font-size:2.1rem; font-weight:800; color:#fff; margin:0 0 8px 0;'>{title}</h2>"
            f"<div style='color:#94a3b8; font-size:0.88rem; margin-bottom:12px; display:flex; gap:10px; align-items:center;'>"
            f"<span>📅 {year_str}</span><span>•</span><span style='color:#facc15; font-weight:700;'>★ {rating:.1f}</span><span>•</span><span>{genres}</span>"
            f"</div>"
            f"<p style='color:#cbd5e1; font-size:0.96rem; line-height:1.6; margin-bottom:20px;'>{overview}</p>",
            unsafe_allow_html=True
        )
        
        row1_c1, row1_c2 = st.columns(2)
        with row1_c1:
            st.markdown(f"<a href='{trailer_url}' target='_blank' class='pickme-btn-red' style='width:100%;'>🎞 &nbsp; TRAILER</a>", unsafe_allow_html=True)
        with row1_c2:
            if st.button("▶ WATCH / FULL DETAILS", key="pickme_details_btn", use_container_width=True):
                st.session_state.selected_movie_id = mid
                st.session_state.active_tab = "Movie Details"
                st.rerun()
        
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 GET ANOTHER RECOMMENDATION", key="pickme_next_rec_btn", use_container_width=True):
            if candidates and len(candidates) > 0:
                st.session_state.quiz_index = (st.session_state.quiz_index + 1) % len(candidates)
            else:
                st.session_state.night_current_pick = sample_night_pick()
            st.rerun()
            
        st.markdown(
            "<div style='text-align:center; color:#64748b; font-size:0.8rem; margin-top:16px; border-top:1px solid #1c263e; padding-top:12px;'>"
            "Powered by MovieMind AI Machine Learning & TMDB Engine 🍿"
            "</div>",
            unsafe_allow_html=True
        )

# Netflix-style Horizontal Carousel with Scroll Animation & Navigation Arrows
def render_netflix_carousel(slider_id, section_title, movie_items, is_top10=False):
    if not movie_items:
        return
    # Parallel batch fetch details for 10x faster rendering
    details_list = tmdb_client.get_batch_movie_details(movie_items)
    
    cards_html = []
    for idx, (item, details) in enumerate(zip(movie_items, details_list)):
        title = item.get('title', 'Movie')
        clean_title = item.get('clean_title', title)
        safe_title = html.escape(str(clean_title))
        raw_year = item.get('year', '2024')
        year_str = str(int(raw_year)) if raw_year and not pd.isna(raw_year) else "2024"
        rating = item.get('avg_rating', 8.0)
        if item.get("is_external"):
            rating *= 2
        tmdb_id = int(item.get('tmdbId', 0))
        genres = item.get('genres_str', '')
        g_chips = "".join([f"<span class='genre-chip'>{g.strip()}</span>" for g in genres.split(',')[:2]])
        poster = html.escape(str(details.get('poster_path') or ""), quote=True)
        source_badge = "TMDB Live" if item.get("is_external") else "MovieLens"
        
        if is_top10:
            rank = idx + 1
            card_code = (
                f"<div class='top10-item-wrap'>"
                f"<div class='top10-huge-num'>{rank}</div>"
                f"<div class='top10-card'>"
                f"<div class='top10-poster'>"
                f"<img src='{poster}' alt='{safe_title}' loading='lazy' />"
                f"<div class='netflix-badge-red'>{source_badge}</div>"
                f"</div>"
                f"<div style='padding:8px 10px;'>"
                f"<div style='font-size:0.86rem; font-weight:700; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{safe_title}</div>"
                f"<div style='font-size:0.75rem; color:#94a3b8; display:flex; justify-content:space-between; margin-top:2px;'>"
                f"<span>{year_str}</span><span style='color:#facc15; font-weight:700;'>★ {rating:.1f}</span>"
                f"</div>"
                f"</div>"
                f"</div>"
                f"</div>"
            )
        else:
            badge_text = "TMDB Live" if item.get("is_external") else "MovieLens"
            badge_color = "#e50914" if item.get("is_external") else "#10b981"
            card_code = (
                f"<div class='n-card'>"
                f"<div class='n-poster-box'>"
                f"<img src='{poster}' alt='{safe_title}' loading='lazy' />"
                f"<div class='heart-badge'>♡</div>"
                f"<div style='position:absolute; bottom:8px; left:8px; background:{badge_color}; color:#fff; font-size:0.65rem; font-weight:800; padding:2px 7px; border-radius:3px; text-transform:uppercase;'>{badge_text}</div>"
                f"</div>"
                f"<div class='card-info'>"
                f"<div class='card-title' title='{safe_title}'>{safe_title}</div>"
                f"<div class='card-sub'>"
                f"<span>{year_str}</span>"
                f"<span style='color:#facc15; font-weight:700;'>★ {rating:.1f}</span>"
                f"</div>"
                f"<div class='card-genres'>{g_chips}</div>"
                f"</div>"
                f"</div>"
            )
        cards_html.append(card_code)

    all_cards = "".join(cards_html)
    
    html = (
        f"<div class='netflix-section'>"
        f"<div class='netflix-section-header'>"
        f"<h3 class='netflix-section-title'>{section_title}</h3>"
        f"<span style='color:#00d2ff; font-size:0.85rem; font-weight:600; cursor:pointer;'>Explore All →</span>"
        f"</div>"
        f"<div class='netflix-slider-wrap'>"
        f"<button class='netflix-nav-arrow arrow-prev' onclick=\"document.getElementById('{slider_id}').scrollBy({{left: -650, behavior: 'smooth'}})\">&#8249;</button>"
        f"<div class='netflix-slider-track' id='{slider_id}'>"
        f"{all_cards}"
        f"</div>"
        f"<button class='netflix-nav-arrow arrow-next' onclick=\"document.getElementById('{slider_id}').scrollBy({{left: 650, behavior: 'smooth'}})\">&#8250;</button>"
        f"</div>"
        f"</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


# ----------------- SIDEBAR -----------------
with st.sidebar:
    # App Logo Header matching Image
    st.markdown(
        "<div style='display:flex; align-items:center; gap:12px; margin-bottom:24px; padding-left:4px;'>"
        "<div style='width:38px; height:38px; border-radius:50%; background:linear-gradient(135deg, #00d2ff, #2563eb); display:flex; align-items:center; justify-content:center; box-shadow:0 0 14px rgba(0, 210, 255, 0.45); font-size:1.25rem;'>🎬</div>"
        "<div><div style='font-size:1.35rem; font-weight:800; color:#fff; line-height:1.1;'>MovieMind <span style='color:#00d2ff;'>AI</span></div>"
        "<div style='font-size:0.75rem; color:#64748b; font-weight:500; letter-spacing:0.3px;'>Discover Beyond Limits</div></div>"
        "</div>",
        unsafe_allow_html=True
    )

    nav_options = [
        "Home",
        "AI Movie Picker",
        "Curated Film Lists",
        "Search & Explore",
        "Recommendations",
        "My Watchlist",
        "My Ratings",
        "Movie Details",
        "Analytics",
        "About",
        "Settings"
    ]
    
    choice = st.radio(
        "Navigation",
        nav_options,
        index=nav_options.index(st.session_state.active_tab) if st.session_state.active_tab in nav_options else 0,
        label_visibility="collapsed"
    )
    st.session_state.active_tab = choice

    # Guest User Profile Box matching Image
    rated_count = len(st.session_state.user_ratings)
    st.markdown(
        "<div class='guest-user-box'>"
        "<div style='display:flex; align-items:center; gap:10px; margin-bottom:6px;'>"
        "<div style='width:32px; height:32px; border-radius:50%; background:#1c263e; display:flex; align-items:center; justify-content:center; color:#94a3b8; font-size:0.9rem;'>👤</div>"
        "<div style='font-weight:700; font-size:0.92rem; color:#fff;'>Guest User</div>"
        "</div>"
        "<div style='font-size:0.78rem; color:#94a3b8; line-height:1.4;'>Login to save your ratings and watchlist</div>"
        "<div class='guest-btn'>Login / Sign Up &nbsp; →</div>"
        "</div>",
        unsafe_allow_html=True
    )
    
    has_api = bool(tmdb_client.api_key)
    badge = "🟢 TMDB Live Connected" if has_api else "⚡ Offline Mode"
    st.caption(f"Poster Engine: {badge}")

# ----------------- TOP HEADER SEARCH BAR -----------------
top_col1, top_col2 = st.columns([5, 1])
with top_col1:
    quick_search = st.text_input(
        "Search",
        placeholder="🔍  Search for movies, genres, or actors...",
        label_visibility="collapsed",
        key="global_search_input"
    )
    if quick_search:
        st.session_state.active_tab = "Search & Explore"
        st.session_state.search_term = quick_search
with top_col2:
    st.markdown(
        "<div style='display:flex; justify-content:flex-end; gap:12px; align-items:center; height:38px;'>"
        "<div class='icon-btn'>🔔</div>"
        "<div class='icon-btn' style='background:linear-gradient(135deg, #2563eb, #00d2ff); color:#fff; font-weight:700;'>👤</div>"
        "</div>",
        unsafe_allow_html=True
    )

# ==========================================
# 1. HOME DASHBOARD
# ==========================================
if st.session_state.active_tab == "Home":
    # Hero Banner matching Image 1:1
    st.markdown(
        "<div class='hero-container'>"
        "<div class='featured-pill'>FEATURED MOVIE</div>"
        "<div class='hero-movie-title'><span class='title-white'>Inter</span><span class='title-cyan'>stellar</span></div>"
        "<div class='hero-desc'>A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.</div>"
        "<div class='hero-meta'>"
        "<span class='hero-star'>★ 8.6</span><span>|</span><span>2014</span><span>|</span><span>Sci-Fi</span><span>|</span><span>Adventure</span><span>|</span><span>Drama</span>"
        "</div>"
        "<div class='hero-actions'>"
        "<a href='https://www.youtube.com/watch?v=zSWdZVtXT7E' target='_blank' class='btn-trailer'>▶ &nbsp; Watch Trailer</a>"
        "<a href='#' class='btn-watchlist'>+ &nbsp; Add to Watchlist</a>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    # 4 Stat Cards Row matching Image 1:1
    st.markdown(
        "<div class='stats-grid'>"
        "<div class='stat-card-box'>"
        "<div class='stat-icon-circle'>🎞️</div>"
        "<div><div class='stat-number'>9,742</div><div class='stat-label-text'>Movies in Dataset</div></div>"
        "</div>"
        "<div class='stat-card-box'>"
        "<div class='stat-icon-circle'>⭐</div>"
        "<div><div class='stat-number'>100,836</div><div class='stat-label-text'>Verified Ratings</div></div>"
        "</div>"
        "<div class='stat-card-box'>"
        "<div class='stat-icon-circle'>🧠</div>"
        "<div><div class='stat-number'>Hybrid ML</div><div class='stat-label-text'>Content + Collaborative</div></div>"
        "</div>"
        "<div class='stat-card-box'>"
        "<div class='stat-icon-circle'>📊</div>"
        "<div><div class='stat-number'>88.0%</div><div class='stat-label-text'>Top-5 Hit Rate</div></div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    # Quick Decision Bar (NightPicks + PickAMovie feature highlight)
    st.markdown(
        "<div style='background:linear-gradient(90deg, #0e1424, #121b33); border:1px solid #1f2d4d; border-radius:14px; padding:18px 22px; margin-bottom:24px;'>"
        "<div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;'>"
        "<div>"
        "<div style='font-size:1.18rem; font-weight:800; color:#fff;'>🎲 Stop scrolling. Just pick something.</div>"
        "<div style='font-size:0.84rem; color:#94a3b8;'>Tired of endless browsing? Use our instant randomized decider or take the 1-minute AI quiz.</div>"
        "</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    q_col1, q_col2, q_col3, q_col4, q_col5, q_col6 = st.columns(6)
    with q_col1:
        if st.button("⚡ Under 90M", use_container_width=True, key="home_btn_u90"):
            st.session_state.picker_sub_mode = "🔀 NightPicks Instant Generator"
            st.session_state.night_current_pick = sample_night_pick(preset="under_90")
            st.session_state.night_pick_requested = True
            st.session_state.active_tab = "AI Movie Picker"
            st.rerun()
    with q_col2:
        if st.button("⭐ Highly Rated", use_container_width=True, key="home_btn_hr"):
            st.session_state.picker_sub_mode = "🔀 NightPicks Instant Generator"
            st.session_state.night_current_pick = sample_night_pick(preset="highly_rated")
            st.session_state.night_pick_requested = True
            st.session_state.active_tab = "AI Movie Picker"
            st.rerun()
    with q_col3:
        if st.button("💑 Date Night", use_container_width=True, key="home_btn_dn"):
            st.session_state.picker_sub_mode = "🔀 NightPicks Instant Generator"
            st.session_state.night_current_pick = sample_night_pick(preset="date_night")
            st.session_state.night_pick_requested = True
            st.session_state.active_tab = "AI Movie Picker"
            st.rerun()
    with q_col4:
        if st.button("💎 Hidden Gem", use_container_width=True, key="home_btn_hg"):
            st.session_state.picker_sub_mode = "🔀 NightPicks Instant Generator"
            st.session_state.night_current_pick = sample_night_pick(preset="hidden_gem")
            st.session_state.night_pick_requested = True
            st.session_state.active_tab = "AI Movie Picker"
            st.rerun()
    with q_col5:
        if st.button("🔀 Instant Pick", use_container_width=True, key="home_btn_spin"):
            st.session_state.picker_sub_mode = "🔀 NightPicks Instant Generator"
            st.session_state.night_current_pick = sample_night_pick()
            st.session_state.night_pick_requested = True
            st.session_state.active_tab = "AI Movie Picker"
            st.rerun()
    with q_col6:
        if st.button("🎯 AI Quiz Wizard", use_container_width=True, key="home_btn_quiz"):
            st.session_state.picker_sub_mode = "🎯 PickAMovie Quiz Wizard"
            st.session_state.active_tab = "AI Movie Picker"
            st.rerun()

    st.markdown(
        "<h3 style='margin:20px 0 16px 0; font-size:1.35rem; font-weight:700; color:#fff;'>"
        "🆕 Latest Movie Releases (TMDB live catalog)</h3>",
        unsafe_allow_html=True,
    )
    try:
        latest_results = get_live_movie_page(
            "primary_release_date.desc",
            f"{date.today().year - 1}-01-01",
            date.today().isoformat(),
        )
        latest_items = [normalize_tmdb_movie(item) for item in latest_results]
        if latest_items:
            render_netflix_carousel(
                "slider-live-latest", "🆕 Recently released movies", latest_items
            )
        else:
            st.info("TMDB did not return recent releases for this period.")
    except RuntimeError as error:
        st.warning(f"Live movie updates are unavailable: {error}")

    # Curated MovieLens examples (not a live trending ranking).
    trending_items = [
        {"title": "Dune: Part Two", "clean_title": "Dune: Part Two", "year": 2024, "avg_rating": 8.5, "genres_str": "Sci-Fi, Adventure"},
        {"title": "Deadpool & Wolverine", "clean_title": "Deadpool & Wolverine", "year": 2024, "avg_rating": 7.8, "genres_str": "Action, Comedy"},
        {"title": "Inside Out 2", "clean_title": "Inside Out 2", "year": 2024, "avg_rating": 7.6, "genres_str": "Animation, Family"},
        {"title": "A Quiet Place: Day One", "clean_title": "A Quiet Place: Day One", "year": 2024, "avg_rating": 7.5, "genres_str": "Horror, Thriller"},
        {"title": "Kingdom of the Planet of the Apes", "clean_title": "Kingdom of the Planet of the Apes", "year": 2024, "avg_rating": 7.4, "genres_str": "Action, Adventure"},
        {"title": "The Fall Guy", "clean_title": "The Fall Guy", "year": 2024, "avg_rating": 7.1, "genres_str": "Action, Comedy"},
        {"title": "Furiosa: A Mad Max Saga", "clean_title": "Furiosa: A Mad Max Saga", "year": 2024, "avg_rating": 7.8, "genres_str": "Action, Adventure"},
        {"title": "Godzilla x Kong: The New Empire", "clean_title": "Godzilla x Kong: The New Empire", "year": 2024, "avg_rating": 6.8, "genres_str": "Action, Sci-Fi"},
        {"title": "Interstellar", "clean_title": "Interstellar", "year": 2014, "avg_rating": 8.6, "genres_str": "Sci-Fi, Adventure"},
        {"title": "Inception", "clean_title": "Inception", "year": 2010, "avg_rating": 8.8, "genres_str": "Sci-Fi, Action"},
        {"title": "The Dark Knight", "clean_title": "The Dark Knight", "year": 2008, "avg_rating": 9.0, "genres_str": "Action, Crime"},
        {"title": "The Martian", "clean_title": "The Martian", "year": 2015, "avg_rating": 8.0, "genres_str": "Sci-Fi, Adventure"}
    ]
    render_netflix_carousel(
        "slider-trending", "🎞️ Popular MovieLens examples", trending_items,
        is_top10=False,
    )

    # 2. Top 10 Movies Today with Giant Outlined Numbers (Netflix Signature)
    top10_items = [
        {"title": "The Dark Knight", "clean_title": "The Dark Knight", "year": 2008, "avg_rating": 9.0, "genres_str": "Action, Crime"},
        {"title": "Interstellar", "clean_title": "Interstellar", "year": 2014, "avg_rating": 8.6, "genres_str": "Sci-Fi, Adventure"},
        {"title": "Inception", "clean_title": "Inception", "year": 2010, "avg_rating": 8.8, "genres_str": "Sci-Fi, Action"},
        {"title": "Pulp Fiction", "clean_title": "Pulp Fiction", "year": 1994, "avg_rating": 8.9, "genres_str": "Crime, Thriller"},
        {"title": "Fight Club", "clean_title": "Fight Club", "year": 1999, "avg_rating": 8.8, "genres_str": "Drama, Thriller"},
        {"title": "The Matrix", "clean_title": "The Matrix", "year": 1999, "avg_rating": 8.7, "genres_str": "Sci-Fi, Action"},
        {"title": "Dune: Part Two", "clean_title": "Dune: Part Two", "year": 2024, "avg_rating": 8.5, "genres_str": "Sci-Fi, Adventure"},
        {"title": "Avengers: Endgame", "clean_title": "Avengers: Endgame", "year": 2019, "avg_rating": 8.4, "genres_str": "Action, Adventure"},
        {"title": "The Martian", "clean_title": "The Martian", "year": 2015, "avg_rating": 8.0, "genres_str": "Sci-Fi, Adventure"},
        {"title": "Toy Story", "clean_title": "Toy Story", "year": 1995, "avg_rating": 8.3, "genres_str": "Animation, Comedy"}
    ]
    render_netflix_carousel(
        "slider-top10", "🏆 MovieLens community favorites (sample titles)",
        top10_items, is_top10=True,
    )

    # 3. Popular Genres Bar with Colorful Themed Badges
    st.markdown("<h3 style='margin:20px 0 16px 0; font-size:1.35rem; font-weight:700; color:#fff;'>🗂️ Popular Genres</h3>", unsafe_allow_html=True)
    st.markdown(
        "<div class='genre-palette-grid'>"
        "<div class='genre-pill-btn g-action'>🎬 Action</div>"
        "<div class='genre-pill-btn g-adv'>🧭 Adventure</div>"
        "<div class='genre-pill-btn g-scifi'>🪐 Sci-Fi</div>"
        "<div class='genre-pill-btn g-drama'>🎭 Drama</div>"
        "<div class='genre-pill-btn g-comedy'>😊 Comedy</div>"
        "<div class='genre-pill-btn g-thriller'>🧬 Thriller</div>"
        "<div class='genre-pill-btn g-horror'>👻 Horror</div>"
        "<div class='genre-pill-btn g-romance'>💖 Romance</div>"
        "<div class='genre-pill-btn g-anim'>🎨 Animation</div>"
        "<div class='genre-pill-btn g-crime'>🕵️ Crime</div>"
        "</div>",
        unsafe_allow_html=True
    )

    # 4. Hybrid ML Recommendations in Netflix Carousel!
    # Reuse the home recommendation result across Streamlit reruns. It only
    # changes when the guest ratings change, avoiding repeated cosine-similarity
    # and collaborative-filtering work on every button interaction.
    rating_signature = tuple(sorted((int(k), float(v)) for k, v in st.session_state.user_ratings.items()))
    if st.session_state.home_recommendation_signature != rating_signature:
        st.session_state.home_recommendations = hybrid_model.recommend(
            movie_id=109487,
            custom_ratings=st.session_state.user_ratings,
            top_n=10,
        )
        st.session_state.home_recommendation_signature = rating_signature
    home_recs = st.session_state.home_recommendations
    rec_items = home_recs.to_dict('records')
    render_netflix_carousel("slider-recommended", "✨ Recommended For You (Hybrid ML Engine)", rec_items, is_top10=False)

    # 5. Handcrafted Film Collections Showcase (MovieDecider)
    st.markdown("<h3 style='margin:28px 0 14px 0; font-size:1.35rem; font-weight:700; color:#fff;'>📚 Curated Film Collections</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-top:-8px; margin-bottom:18px;'>Handcrafted themed lists built around moods, occasions, and hidden masterworks.</p>", unsafe_allow_html=True)
    
    dec_c1, dec_c2, dec_c3, dec_c4 = st.columns(4)
    preview_lists = [
        ("under-90", "⏱️ Great Films Under 90 Mins", "Finish in under 1.5 hours — whole story without a whole evening.", dec_c1),
        ("hidden-gems", "💎 Hidden Gems: Almost Nobody Has Seen", "Films with supreme ratings but a fraction of mainstream audience.", dec_c2),
        ("scifi-think", "🧠 Sci-Fi That Makes You Think", "Built on mind-bending concepts rather than mindless explosions.", dec_c3),
        ("best-90s", "📼 The Best Films of the 1990s", "The golden decade of independent cinema and auteur masterworks.", dec_c4)
    ]
    for lid, ltitle, ldesc, lcol in preview_lists:
        with lcol:
            st.markdown(
                f"<div class='decider-box' style='min-height:175px;'>"
                f"<div>"
                f"<div class='decider-pill'>{CURATED_LISTS[lid]['badge']}</div>"
                f"<div class='decider-title' style='font-size:1.05rem;'>{ltitle}</div>"
                f"<div class='decider-desc' style='font-size:0.82rem;'>{ldesc}</div>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            if st.button("Explore List →", key=f"home_dec_{lid}", use_container_width=True):
                st.session_state.selected_curated_list = lid
                st.session_state.active_tab = "Curated Film Lists"
                st.rerun()

# ==========================================
# 2. AI MOVIE PICKER (NightPicks + PickAMovie)
# ==========================================
elif st.session_state.active_tab == "AI Movie Picker":
    if "picker_sub_mode" not in st.session_state:
        st.session_state.picker_sub_mode = "🔀 NightPicks Instant Generator"

    mode_c1, mode_c2 = st.columns(2)
    with mode_c1:
        is_np = (st.session_state.picker_sub_mode == "🔀 NightPicks Instant Generator")
        if st.button("🔀  NightPicks Instant Generator", type="primary" if is_np else "secondary", use_container_width=True, key="btn_submode_np"):
            st.session_state.picker_sub_mode = "🔀 NightPicks Instant Generator"
            st.rerun()
    with mode_c2:
        is_qz = (st.session_state.picker_sub_mode == "🎯 PickAMovie Quiz Wizard")
        if st.button("🎯  PickAMovie Quiz Wizard", type="primary" if is_qz else "secondary", use_container_width=True, key="btn_submode_qz"):
            st.session_state.picker_sub_mode = "🎯 PickAMovie Quiz Wizard"
            st.rerun()

    if st.session_state.picker_sub_mode == "🔀 NightPicks Instant Generator":
        st.markdown(
            "<div class='night-hero-box'>"
            "<div class='night-main-title'>Random Movie Generator</div>"
            "<div class='night-sub-text'>Stop scrolling. Start watching. The fastest way to decide what to watch tonight.</div>"
            "</div>",
            unsafe_allow_html=True
        )

        # Preset Quick Chips Row
        p_c1, p_c2, p_c3, p_c4 = st.columns(4)
        with p_c1:
            if st.button("⚡ UNDER 90M", use_container_width=True, key="np_preset_u90"):
                st.session_state.night_current_pick = sample_night_pick(preset="under_90")
                st.session_state.night_pick_requested = True
                st.rerun()
        with p_c2:
            if st.button("⭐ HIGHLY RATED", use_container_width=True, key="np_preset_hr"):
                st.session_state.night_current_pick = sample_night_pick(preset="highly_rated")
                st.session_state.night_pick_requested = True
                st.rerun()
        with p_c3:
            if st.button("💑 DATE NIGHT", use_container_width=True, key="np_preset_dn"):
                st.session_state.night_current_pick = sample_night_pick(preset="date_night")
                st.session_state.night_pick_requested = True
                st.rerun()
        with p_c4:
            if st.button("💎 HIDDEN GEM", use_container_width=True, key="np_preset_hg"):
                st.session_state.night_current_pick = sample_night_pick(preset="hidden_gem")
                st.session_state.night_pick_requested = True
                st.rerun()

        # Customizable Search Filters Expander
        with st.expander("🎛️ Customize Search & Streaming Filters", expanded=False):
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                all_genre_opts = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", 
                                  "Drama", "Family", "Fantasy", "Horror", "Mystery", "Romance", 
                                  "Sci-Fi", "Thriller", "War", "Western"]
                chosen_mood = st.selectbox("I'm in the mood for...", ["All / Any"] + all_genre_opts, index=0)
            with f_col2:
                chosen_era = st.selectbox("Era", ["Any Era", "70s", "80s", "90s", "00s", "10s", "20s"], index=0)
            with f_col3:
                chosen_stream = st.selectbox(
                    "Streaming Platform",
                    ["All Available", "Netflix", "Prime Video", "Disney+ Hotstar", "Apple TV+"],
                )

            s_col1, s_col2 = st.columns(2)
            with s_col1:
                chosen_min_rat = st.slider("Minimum Rating", 0.0, 9.0, 6.5, 0.5, key="np_slider_rat")
            with s_col2:
                chosen_sort = st.selectbox("Sort Priority", ["Popularity", "Top Rated", "Newest"])

        # Big Action Button
        _, spin_col, _ = st.columns([1, 2, 1])
        with spin_col:
            if st.button("🔀  Pick a Movie / Spin Again", type="primary", use_container_width=True, key="np_big_spin_btn"):
                mood_arg = None if chosen_mood == "All / Any" else chosen_mood
                era_arg = None if chosen_era == "Any Era" else chosen_era
                provider_arg = (
                    None if chosen_stream == "All Available" else chosen_stream
                )
                st.session_state.night_current_pick = sample_night_pick(
                    mood=mood_arg,
                    era=era_arg,
                    min_rating=chosen_min_rat,
                    sort_by=chosen_sort,
                    streaming_provider=provider_arg,
                )
                st.session_state.night_pick_requested = True
                st.rerun()

        # Render Active Pick
        if (
            st.session_state.night_current_pick is None
            and not st.session_state.get("night_pick_requested", False)
        ):
            st.session_state.night_current_pick = sample_night_pick(preset="highly_rated")
            st.session_state.night_pick_requested = True

        active_movie = st.session_state.night_current_pick
        if active_movie is None:
            st.warning(
                st.session_state.get(
                    "night_picker_error",
                    "No movie matches these filters. Please adjust your selection.",
                )
            )
        else:
            render_night_result_card(active_movie)

        # "View more like this" Expander
        if active_movie is not None:
            with st.expander("▾ View more like this", expanded=False):
                if not active_movie.get("is_external"):
                    similar_to_pick = cb_model.recommend_by_movie_id(
                        int(active_movie.get('movieId', 109487)), top_n=6
                    )
                    if not similar_to_pick.empty:
                        v_cols = st.columns(6)
                        for idx, (_, r) in enumerate(similar_to_pick.iterrows()):
                            render_movie_card(
                                r, col_obj=v_cols[idx],
                                card_key=f"more_like_{idx}_{r['movieId']}",
                            )
                else:
                    st.info(
                        "This live TMDB movie is not in the MovieLens training data yet, "
                        "so similarity recommendations are unavailable."
                    )

        # 4 Steps Row matching Image 1:1
        st.markdown(
            "<div class='night-steps-grid'>"
            "<div class='night-step-card'><div class='night-step-num'>01</div><div class='night-step-title'>Pick in seconds</div><div class='night-step-desc'>One spin. No trailers to hunt down, no endless rows to scroll.</div></div>"
            "<div class='night-step-card'><div class='night-step-num'>02</div><div class='night-step-title'>Filter by mood</div><div class='night-step-desc'>Horror under 90 min. Comedy rated 7+. Family film on Netflix. Stack it until it fits.</div></div>"
            "<div class='night-step-card'><div class='night-step-num'>03</div><div class='night-step-title'>Know where to watch</div><div class='night-step-desc'>Every result shows which services have it in your region. No separate search.</div></div>"
            "<div class='night-step-card'><div class='night-step-num'>04</div><div class='night-step-title'>Preview first</div><div class='night-step-desc'>Watch the trailer before committing. Not right? Spin again — it takes two seconds.</div></div>"
            "</div>",
            unsafe_allow_html=True
        )

        # Browse Categories & Streaming Services Cards matching Image
        st.markdown("<h4 style='color:#fff; margin-top:25px;'>Browse by genre, streaming service, or franchise</h4>", unsafe_allow_html=True)
        cat_c1, cat_c2, cat_c3 = st.columns(3)
        with cat_c1:
            st.markdown("<div class='cat-card-item'><div>🎬</div><div><div style='color:#fff; font-weight:700;'>Action</div><div style='color:#64748b; font-size:0.75rem;'>Big energy picks</div></div></div>", unsafe_allow_html=True)
            st.markdown("<div class='cat-card-item' style='margin-top:10px;'><div>💖</div><div><div style='color:#fff; font-weight:700;'>Romance</div><div style='color:#64748b; font-size:0.75rem;'>Date night favorites</div></div></div>", unsafe_allow_html=True)
        with cat_c2:
            st.markdown("<div class='cat-card-item'><div>😂</div><div><div style='color:#fff; font-weight:700;'>Comedy</div><div style='color:#64748b; font-size:0.75rem;'>Light and funny picks</div></div></div>", unsafe_allow_html=True)
            st.markdown("<div class='cat-card-item' style='margin-top:10px;'><div>🕵️</div><div><div style='color:#fff; font-weight:700;'>Thriller</div><div style='color:#64748b; font-size:0.75rem;'>Tense and gripping picks</div></div></div>", unsafe_allow_html=True)
        with cat_c3:
            st.markdown("<div class='cat-card-item'><div>⏱️</div><div><div style='color:#fff; font-weight:700;'>Under 90 Minutes</div><div style='color:#64748b; font-size:0.75rem;'>Quick movie night picks</div></div></div>", unsafe_allow_html=True)
            st.markdown("<div class='cat-card-item' style='margin-top:10px;'><div>📺</div><div><div style='color:#fff; font-weight:700;'>Streaming Picks</div><div style='color:#64748b; font-size:0.75rem;'>Netflix, Prime & Disney+</div></div></div>", unsafe_allow_html=True)

    else:
        st.markdown("## 🎯 AI Matchmaker & Movie Quiz")
        st.markdown("Answer a few quick questions and let our Hybrid ML system compute your ideal movie match.")

        # Interactive Zero-Lag Form: users can click all choices instantly without page reload lag!
        with st.form("quiz_matchmaker_form"):
            q_col1, q_col2 = st.columns(2)
            with q_col1:
                mood_labels = [m['label'] for m in QUIZ_MOODS]
                selected_mood_label = st.radio("1. What's your vibe or mood?", mood_labels, index=0)
                
                occasion_labels = [o['label'] for o in QUIZ_OCCASIONS]
                selected_occ_label = st.radio("2. Who are you watching with?", occasion_labels, index=0)

            with q_col2:
                selected_theme = st.selectbox("3. Any specific theme or angle?", QUIZ_SPECIAL_THEMES, index=0)
                selected_quiz_era = st.selectbox("4. Era Preference", QUIZ_ERAS, index=0)
                min_quiz_rating = st.slider("5. Minimum Rating", 0.0, 9.0, 7.0, 0.5, key="quiz_min_rat")

            quiz_submit_btn = st.form_submit_button("🎲  FIND MY PERFECT MOVIE", type="primary", use_container_width=True)

        if quiz_submit_btn:
            chosen_mood_obj = next((m for m in QUIZ_MOODS if m['label'] == selected_mood_label), QUIZ_MOODS[0])
            req_genres = chosen_mood_obj.get('genres', [])
            
            q_thresh = (min_quiz_rating / 2.0) if min_quiz_rating > 5.0 else min_quiz_rating
            df = movies_df.copy()
            if req_genres:
                requested_genres = {genre.casefold() for genre in req_genres}
                df = df[
                    df["genres"].fillna("").str.split("|").apply(
                        lambda genres: bool(
                            requested_genres
                            & {genre.casefold() for genre in genres}
                        )
                    )
                ]
            df = df[df["avg_rating"] >= q_thresh]

            occasion = next(
                (item for item in QUIZ_OCCASIONS if item["label"] == selected_occ_label),
                QUIZ_OCCASIONS[0],
            )["value"]
            occasion_genres = {
                "date": {"Romance", "Comedy"},
                "friends": {"Comedy", "Action", "Adventure"},
                "family": {"Animation", "Children", "Family"},
            }.get(occasion)
            if occasion_genres:
                df = df[
                    df["genres"].fillna("").str.split("|").apply(
                        lambda genres: bool(
                            {genre.casefold() for genre in genres}
                            & {genre.casefold() for genre in occasion_genres}
                        )
                    )
                ]

            if selected_quiz_era.startswith("Modern"):
                df = df[df["year"].between(2015, date.today().year)]
            elif selected_quiz_era.startswith("The 2000s"):
                df = df[df["year"].between(2000, 2014)]
            elif selected_quiz_era.startswith("90s"):
                df = df[df["year"].between(1990, 1999)]
            elif selected_quiz_era.startswith("Vintage"):
                df = df[df["year"] < 1990]

            theme_filters = {
                "Space": ("space|alien", "Sci-Fi"),
                "Heist": ("heist|robbery", "Crime"),
                "Mind-Bending": ("twist|mindfuck", "Mystery"),
                "True Stories": ("biography|true story", "Drama|Documentary"),
                "Fast Cars": ("racing|cars?|driving", "Action"),
                "Hard-Boiled": ("detective|noir", "Film-Noir|Crime|Mystery"),
            }
            theme = next(
                (
                    value for label, value in theme_filters.items()
                    if label in selected_theme
                ),
                None,
            )
            if theme:
                tag_pattern, genre_pattern = theme
                theme_matches = (
                    df["tag"].fillna("").str.contains(
                        tag_pattern, case=False, regex=True
                    )
                    | df["genres"].fillna("").str.contains(
                        genre_pattern, case=False, regex=True
                    )
                )
                df = df[theme_matches]
            elif "Highest-Rated Community" in selected_theme:
                df = df[(df["avg_rating"] >= 4.3) & (df["rating_count"] >= 100)]

            df = df.sort_values(
                by=['avg_rating', 'rating_count'], ascending=[False, False]
            )
            st.session_state.quiz_candidates = df.head(15).to_dict('records')
            st.session_state.quiz_submitted = True
            if not st.session_state.quiz_candidates:
                st.session_state.quiz_error = (
                    "No movies match every quiz answer in the current catalog. "
                    "Try relaxing one or more answers."
                )
            else:
                st.session_state.quiz_error = None
            st.session_state.quiz_index = 0
            st.rerun()

        if (
            not st.session_state.quiz_candidates
            and not st.session_state.get("quiz_submitted", False)
        ):
            default_cand = movies_df[movies_df['title'].str.contains("War Dogs", case=False, na=False)]
            if not default_cand.empty:
                st.session_state.quiz_candidates = default_cand.to_dict('records')
            else:
                st.session_state.quiz_candidates = movies_df[movies_df['avg_rating'] >= 4.0].head(10).to_dict('records')

        if st.session_state.get("quiz_error"):
            st.warning(st.session_state.quiz_error)
        if st.session_state.quiz_candidates:
            current_idx = st.session_state.quiz_index % len(st.session_state.quiz_candidates)
            curr_match = st.session_state.quiz_candidates[current_idx]
            
            # War Dogs result card matching image 1:1
            render_pickme_result_card(curr_match, st.session_state.quiz_candidates, current_idx)
            
            # Underneath: runner-up carousel (super fast parallel fetch)
            runners_up = [c for i, c in enumerate(st.session_state.quiz_candidates) if i != current_idx][:6]
            if runners_up:
                render_netflix_carousel("slider-quiz-runners", "✨ More Top Matches for this Vibe", runners_up, is_top10=False)

# ==========================================
# 3. CURATED FILM LISTS (MovieDecider Style)
# ==========================================
elif st.session_state.active_tab == "Curated Film Lists":
    if st.session_state.selected_curated_list is None:
        st.markdown(
            "<div style='margin-bottom:20px;'>"
            "<div style='font-size:0.82rem; color:#64748b; margin-bottom:8px;'>Home &nbsp;›&nbsp; <span style='color:#00d2ff;'>Lists</span></div>"
            "<h1 style='font-size:2.8rem; font-weight:900; color:#fff; margin:0 0 10px 0;'>Film lists</h1>"
            "<p style='color:#94a3b8; font-size:1.02rem; line-height:1.6; max-width:920px;'>"
            "Genre pages tell you what a film is. These lists try to answer the more useful question — <b>what it is for</b>. "
            "Each one is built around a mood, an occasion or an angle we find genuinely interesting, then filled from our library using our ratings, runtime and audience data."
            "</p>"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown("<h4 style='color:#fff; margin-top:24px; text-transform:uppercase; letter-spacing:0.8px; font-size:0.88rem;'>ALL LISTS</h4>", unsafe_allow_html=True)
        
        list_keys = list(CURATED_LISTS.keys())
        for i in range(0, len(list_keys), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(list_keys):
                    lid = list_keys[i + j]
                    cdata = CURATED_LISTS[lid]
                    with cols[j]:
                        st.markdown(
                            f"<div class='decider-box' style='min-height:220px; margin-bottom:16px;'>"
                            f"<div>"
                            f"<div class='decider-pill'>{cdata['badge']}</div>"
                            f"<div class='decider-title'>{cdata['title']}</div>"
                            f"<div class='decider-desc'>{cdata['short_desc']}</div>"
                            f"</div>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        if st.button("Explore List →", key=f"btn_explore_{lid}", use_container_width=True):
                            st.session_state.selected_curated_list = lid
                            st.rerun()

    else:
        selected_id = st.session_state.selected_curated_list
        cdata = CURATED_LISTS.get(selected_id, CURATED_LISTS["under-90"])
        
        c_back, _ = st.columns([1, 4])
        with c_back:
            if st.button("← Back to All Lists", key="btn_back_to_lists"):
                st.session_state.selected_curated_list = None
                st.rerun()

        if selected_id == "under-90":
            resolved_movies = []
            try:
                filters = {"with_runtime.lte": 89, "vote_count.gte": 20}
                first_page = tmdb_client.discover_movies(
                    page=1, sort_by="popularity.desc", filters=filters
                )
                total_pages = min(int(first_page.get("total_pages", 1)), 500)
                page_number = st.number_input(
                    "Results page", min_value=1, max_value=max(1, total_pages),
                    value=1, step=1, key="under90_results_page",
                )
                page_data = (
                    first_page if page_number == 1 else tmdb_client.discover_movies(
                        page=page_number, sort_by="popularity.desc", filters=filters
                    )
                )
                for candidate in page_data["results"]:
                    title = candidate.get("title") or candidate.get("original_title")
                    release_date = candidate.get("release_date", "")
                    year = int(release_date[:4]) if len(release_date) >= 4 else None
                    details = get_movie_metadata(
                        int(candidate["id"]), title, year
                    )
                    runtime = details.get("runtime")
                    if runtime is None and (
                        tmdb_client.api_key or tmdb_client.read_token
                    ):
                        details = get_movie_metadata(
                            int(candidate["id"]), title, year, refresh=True
                        )
                        runtime = details.get("runtime")
                    if runtime is None or int(runtime) >= 90:
                        continue
                    resolved_movies.append({
                        "movieId": 1_000_000_000 + int(candidate["id"]),
                        "title": f"{title} ({year})" if year else title,
                        "clean_title": title,
                        "year": year,
                        "genres_str": ", ".join(details.get("genres", [])),
                        "avg_rating": float(candidate.get("vote_average") or 0) / 2,
                        "rating_count": int(candidate.get("vote_count") or 0),
                        "tmdbId": int(candidate["id"]),
                        "runtime": int(runtime),
                        "is_external": True,
                    })
                    if len(resolved_movies) == 6:
                        break
                if not resolved_movies:
                    st.info(
                        "No movies with a verified runtime under 90 minutes were found "
                        "on this page. Try another results page."
                    )
            except RuntimeError as error:
                st.warning(str(error))
        else:
            resolved_movies = [resolve_curated_movie(m) for m in cdata['movies']]

        st.markdown(
            f"<div style='font-size:0.82rem; color:#64748b; margin-top:10px; margin-bottom:8px;'>Home &nbsp;›&nbsp; Lists &nbsp;›&nbsp; <span style='color:#00d2ff;'>{cdata['title']}</span></div>"
            f"<h1 style='font-size:2.8rem; font-weight:900; color:#fff; margin:0 0 14px 0;'>{cdata['title']}</h1>"
            f"<div class='decider-editorial-banner'>{cdata['editorial']}</div>"
            f"<div style='margin-bottom:20px; font-weight:800; font-size:0.92rem; color:#38bdf8; text-transform:uppercase; letter-spacing:1px;'>THE LIST - {len(resolved_movies)} VERIFIED FILMS ON THIS PAGE</div>",
            unsafe_allow_html=True
        )

        for row_start in range(0, len(resolved_movies), 6):
            grid_cols = st.columns(6)
            for idx in range(6):
                movie_idx = row_start + idx
                if movie_idx < len(resolved_movies):
                    m_row = resolved_movies[movie_idx]
                    render_movie_card(m_row, col_obj=grid_cols[idx], card_key=f"curated_{selected_id}_{movie_idx}_{m_row['movieId']}")

# ==========================================
# 4. SEARCH & EXPLORE
# ==========================================
elif st.session_state.active_tab == "Search & Explore":
    st.title("🔍 Search & Discover Movies")
    st.markdown("Search through 9,700+ movies or filter by genre, release year, and community rating.")

    c_search, c_sort = st.columns([3, 1])
    with c_search:
        init_term = st.session_state.get('search_term', '')
        search_query = st.text_input("Search Title or Keyword", value=init_term, placeholder="e.g. Inception, Marvel, Matrix, Batman...")
    with c_sort:
        sort_by = st.selectbox("Sort By", ["Highest Rated", "Most Popular", "Newest First", "Title A-Z"])

    with st.expander("⚙️ Advanced Filters (Genre, Year, Rating)", expanded=False):
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            all_genres = ["Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", 
                          "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", 
                          "Sci-Fi", "Thriller", "War", "Western"]
            selected_genres = st.multiselect("Genres", all_genres, default=[])
        with f_col2:
            year_range = st.slider(
                "Release Year", 1888, date.today().year,
                (1980, date.today().year),
            )
        with f_col3:
            min_rating = st.slider("Min Average Rating", 0.0, 5.0, 3.0, 0.5)

    include_live_catalog = st.checkbox(
        "Include current TMDB movies and releases",
        value=True,
        help="Browse the live catalog in pages; TMDB exposes up to 500 pages per query.",
    )
    live_page_number = 1
    live_movies = []
    if include_live_catalog:
        genre_ids = {
            "Action": 28, "Adventure": 12, "Animation": 16, "Children": 10751,
            "Comedy": 35, "Crime": 80, "Documentary": 99, "Drama": 18,
            "Fantasy": 14, "Film-Noir": 9648, "Horror": 27, "Musical": 10402,
            "Mystery": 9648, "Romance": 10749, "Sci-Fi": 878,
            "Thriller": 53, "War": 10752, "Western": 37,
        }
        live_filters = {
            "primary_release_date.gte": f"{year_range[0]}-01-01",
            "primary_release_date.lte": f"{year_range[1]}-12-31",
            "vote_average.gte": min_rating * 2,
            "include_adult": False,
        }
        if selected_genres:
            live_filters["with_genres"] = ",".join(
                str(genre_ids[genre]) for genre in selected_genres
                if genre in genre_ids
            )
        try:
            if search_query.strip():
                live_data = tmdb_client.search_movies(search_query.strip(), page=1)
                live_sort = None
            else:
                live_sort = {
                    "Highest Rated": "vote_average.desc",
                    "Most Popular": "popularity.desc",
                    "Newest First": "primary_release_date.desc",
                    "Title A-Z": "original_title.asc",
                }[sort_by]
                live_data = tmdb_client.discover_movies(
                    page=1, sort_by=live_sort, filters=live_filters
                )
            live_total_pages = min(int(live_data.get("total_pages", 1)), 500)
            live_page_number = st.number_input(
                f"Live TMDB results page (up to {live_total_pages})",
                min_value=1, max_value=max(1, live_total_pages),
                value=1, step=1, key="live_catalog_page",
            )
            if live_page_number != 1:
                if search_query.strip():
                    live_data = tmdb_client.search_movies(
                        search_query.strip(), page=live_page_number
                    )
                else:
                    live_data = tmdb_client.discover_movies(
                        page=live_page_number,
                        sort_by=live_sort,
                        filters=live_filters,
                    )
            live_movies = [normalize_tmdb_movie(item) for item in live_data["results"]]
            if selected_genres:
                live_movies = [
                    item for item in live_movies
                    if all(
                        genre.casefold() in {
                            value.casefold()
                            for value in item["genres"].split("|")
                        }
                        for genre in selected_genres
                        if genre in genre_ids
                    )
                ]
            live_movies = [
                item for item in live_movies
                if item["year"] is not None
                and year_range[0] <= item["year"] <= year_range[1]
                and item["avg_rating"] >= min_rating
            ]
        except RuntimeError as error:
            st.warning(f"Live TMDB results are unavailable: {error}")

    filtered = movies_df.copy()
    if search_query:
        q = search_query.lower().strip()
        filtered = filtered[
            filtered['title'].str.lower().str.contains(q, regex=False) |
            filtered['clean_title'].str.lower().str.contains(q, regex=False) |
            filtered['tag'].str.lower().str.contains(q, regex=False)
        ]

    if selected_genres:
        for g in selected_genres:
            filtered = filtered[filtered['genres'].str.contains(g, case=False, na=False)]

    filtered = filtered[(filtered['year'] >= year_range[0]) & (filtered['year'] <= year_range[1])]
    filtered = filtered[filtered['avg_rating'] >= min_rating]

    if sort_by == "Highest Rated":
        filtered = filtered.sort_values(by=['avg_rating', 'rating_count'], ascending=[False, False])
    elif sort_by == "Most Popular":
        filtered = filtered.sort_values(by=['rating_count', 'avg_rating'], ascending=[False, False])
    elif sort_by == "Newest First":
        filtered = filtered.sort_values(by=['year', 'rating_count'], ascending=[False, False])
    elif sort_by == "Title A-Z":
        filtered = filtered.sort_values(by='clean_title', ascending=True)

    # Quick Curated List Jump Pills matching MovieDecider
    st.markdown("<div style='margin: 12px 0 6px 0; font-size:0.8rem; font-weight:700; color:#64748b; text-transform:uppercase;'>Or start from a curated list</div>", unsafe_allow_html=True)
    l_c1, l_c2, l_c3, l_c4, l_c5 = st.columns(5)
    with l_c1:
        if st.button("⏱️ Under 90 Mins", key="sq_u90", use_container_width=True):
            st.session_state.selected_curated_list = "under-90"
            st.session_state.active_tab = "Curated Film Lists"
            st.rerun()
    with l_c2:
        if st.button("💎 Hidden Gems", key="sq_hg", use_container_width=True):
            st.session_state.selected_curated_list = "hidden-gems"
            st.session_state.active_tab = "Curated Film Lists"
            st.rerun()
    with l_c3:
        if st.button("🧠 Sci-Fi Mind-Benders", key="sq_sf", use_container_width=True):
            st.session_state.selected_curated_list = "scifi-think"
            st.session_state.active_tab = "Curated Film Lists"
            st.rerun()
    with l_c4:
        if st.button("📼 90s Classics", key="sq_90s", use_container_width=True):
            st.session_state.selected_curated_list = "best-90s"
            st.session_state.active_tab = "Curated Film Lists"
            st.rerun()
    with l_c5:
        if st.button("📚 All Lists →", key="sq_all", use_container_width=True):
            st.session_state.selected_curated_list = None
            st.session_state.active_tab = "Curated Film Lists"
            st.rerun()

    st.write(
        f"Found **{len(filtered) + len(live_movies)}** movies matching your criteria "
        f"({len(filtered)} MovieLens, {len(live_movies)} live TMDB on this page)."
    )

    PAGE_SIZE = 12
    total_local_pages = max(1, int(np.ceil(len(filtered) / PAGE_SIZE)))
    local_page_number = st.number_input(
        f"MovieLens results page (up to {total_local_pages})",
        min_value=1,
        max_value=total_local_pages,
        value=1,
        step=1,
        key="movielens_catalog_page",
    )
    local_start = (local_page_number - 1) * PAGE_SIZE
    display_movies = filtered.iloc[local_start:local_start + PAGE_SIZE]
    
    if not display_movies.empty:
        grid_cols = st.columns(6)
        for idx, (_, row) in enumerate(display_movies.iterrows()):
            render_movie_card(row, col_obj=grid_cols[idx % 6], card_key=f"search_{idx}_{row['movieId']}")
    if live_movies:
        st.write(f"**{len(live_movies)} live TMDB titles on page {live_page_number}**")
        live_cols = st.columns(6)
        for idx, row in enumerate(live_movies):
            render_movie_card(
                row,
                col_obj=live_cols[idx % 6],
                card_key=f"live_search_{live_page_number}_{row['tmdbId']}",
            )
    if display_movies.empty and not live_movies:
        st.info("No movies found matching these filters. Try adjusting your search query.")

    # Project Cinema Guides (from MovieDecider)
    st.markdown("<h3 style='margin:35px 0 14px 0; font-size:1.3rem; font-weight:700; color:#fff;'>📖 Guides from the Project</h3>", unsafe_allow_html=True)
    g_exp1, g_exp2, g_exp3 = st.columns(3)
    with g_exp1:
        with st.expander("🤔 Why you can't decide what to watch"):
            st.markdown(
                "**Choice Overload in Modern Streaming**\n\n"
                "When presented with 10,000+ unstructured choices, the human brain suffers from analysis paralysis. "
                "Instead of evaluating movies based on quality, viewers end up picking familiar comfort watches. "
                "MovieMind AI solves this by introducing deliberate constraints (mood, duration, latent affinity)."
            )
    with g_exp2:
        with st.expander("🧠 How our Hybrid ML Engine ranks films"):
            st.markdown(
                "**Mathematical Fusion of Taste**\n\n"
                "Content-Based filtering uses TF-IDF cosine similarity across genres and tags. "
                "Collaborative Filtering analyzes peer ratings from 610 users. Our hybrid score fuses them: "
                "$$Score_{Hybrid} = \\alpha S_{CB} + (1-\\alpha) S_{CF}$$, providing immunity to cold-start."
            )
    with g_exp3:
        with st.expander("⭐ Do IMDb and TMDB agree?"):
            st.markdown(
                "**Dataset Rating Correlation**\n\n"
                "Our cross-database validation shows an 84.2% correlation between TMDB vote averages and IMDb scores. "
                "However, TMDB audiences reward world cinema and independent releases with slightly higher marks."
            )

# ==========================================
# 3. RECOMMENDATIONS
# ==========================================
elif st.session_state.active_tab == "Recommendations":
    st.title("🎯 Personalized Recommendations")
    st.markdown("Tailored movie suggestions powered by machine learning algorithms.")

    rec_mode = st.tabs([
        "🔮 Hybrid Model (Best of Both)",
        "🎬 Content-Based (Similar Movies)",
        "👥 Collaborative (Based on Your Ratings)"
    ])

    with rec_mode[0]:
        st.subheader("Hybrid Recommender Engine")
        st.markdown(
            "Combines **Content-Based feature similarity** (genres, storyline, tags) with **Collaborative user rating patterns**."
        )

        h_col1, h_col2 = st.columns([2, 1])
        with h_col1:
            fav_options = movies_df[movies_df['rating_count'] >= 50].sort_values(by='title')
            seed_movie_name = st.selectbox(
                "Select a movie you love:",
                fav_options['title'].tolist(),
                index=fav_options['title'].tolist().index("Interstellar (2014)") if "Interstellar (2014)" in fav_options['title'].tolist() else 0,
                key="hybrid_seed_select"
            )
            seed_row = fav_options[fav_options['title'] == seed_movie_name].iloc[0]
            seed_mid = int(seed_row['movieId'])

        with h_col2:
            alpha = st.slider(
                "Recommendation Balance (α)",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.05,
                help="1.0 = Pure Content-Based | 0.0 = Pure Collaborative | 0.5 = Equal Blend"
            )
            st.caption(f"Mix: **{int(alpha*100)}% Content** + **{int((1-alpha)*100)}% Collaborative**")

        st.markdown("---")
        
        hybrid_recs = hybrid_model.recommend(
            movie_id=seed_mid,
            custom_ratings=st.session_state.user_ratings,
            alpha=alpha,
            top_n=6
        )

        if not hybrid_recs.empty:
            st.write(f"Top recommended picks based on **{seed_row['clean_title']}**:")
            h_cols = st.columns(6)
            for idx, (_, r) in enumerate(hybrid_recs.iterrows()):
                match_pct = f"{r.get('match_percentage', 85):.0f}% Match"
                render_movie_card(r, score_badge=match_pct, col_obj=h_cols[idx])

    with rec_mode[1]:
        st.subheader("Content-Based Similarity (TF-IDF + Cosine)")
        cb_seed = st.selectbox(
            "Select movie to find similar titles:",
            movies_df[movies_df['rating_count'] >= 30].sort_values(by='title')['title'].tolist(),
            index=0,
            key="cb_seed_select"
        )
        cb_seed_row = movies_df[movies_df['title'] == cb_seed].iloc[0]
        cb_mid = int(cb_seed_row['movieId'])

        cb_recs = cb_model.recommend_by_movie_id(cb_mid, top_n=6)

        if not cb_recs.empty:
            st.write(f"Movies most similar to **{cb_seed_row['clean_title']}**:")
            cb_cols = st.columns(6)
            for idx, (_, r) in enumerate(cb_recs.iterrows()):
                badge = f"{r.get('match_percentage', 80):.1f}% Sim"
                render_movie_card(r, score_badge=badge, col_obj=cb_cols[idx])

    with rec_mode[2]:
        st.subheader("Collaborative Filtering")
        if not st.session_state.user_ratings:
            st.warning("You haven't rated any movies yet! Go to 'My Ratings' tab to rate a few titles.")
        else:
            st.write(f"Personalized picks based on your **{len(st.session_state.user_ratings)} rated movies**:")
            live_cf_recs = cf_model.recommend_for_custom_user(st.session_state.user_ratings, top_n=6)
            if not live_cf_recs.empty:
                cf_cols = st.columns(6)
                for idx, (_, r) in enumerate(live_cf_recs.iterrows()):
                    badge = f"Pred: {r.get('predicted_rating', 4.0):.1f}★"
                    render_movie_card(r, score_badge=badge, col_obj=cf_cols[idx])

# ==========================================
# 4. MY WATCHLIST
# ==========================================
elif st.session_state.active_tab == "My Watchlist":
    st.title("🔖 My Watchlist")
    st.markdown("Your saved movies to watch next.")
    
    # Quick add
    w_add = st.selectbox("Add a movie to watchlist:", movies_df.sort_values(by='title')['title'].tolist())
    if st.button("+ Add to Watchlist"):
        if w_add not in st.session_state.watchlist:
            st.session_state.watchlist.append(w_add)
            st.toast(f"Added {w_add} to your watchlist!", icon="🔖")
            st.rerun()

    if st.session_state.watchlist:
        w_matches = movies_df[movies_df['title'].isin(st.session_state.watchlist)]
        w_cols = st.columns(6)
        for idx, (_, r) in enumerate(w_matches.iterrows()):
            render_movie_card(r, col_obj=w_cols[idx % 6])
    else:
        st.info("Your watchlist is currently empty. Add movies using the dropdown above or from any movie card!")

# ==========================================
# 5. MY RATINGS
# ==========================================
elif st.session_state.active_tab == "My Ratings":
    st.title("🤍 My Ratings")
    st.markdown("Rate movies on a 1-5 star scale to personalize your recommendation engine in real-time.")

    r_col1, r_col2 = st.columns([2, 1])
    with r_col1:
        st.subheader("Rate a Movie")
        search_for_rate = st.selectbox(
            "Select movie to rate:",
            movies_df.sort_values(by=['rating_count', 'title'], ascending=[False, True])['title'].tolist()
        )
        rate_movie_row = movies_df[movies_df['title'] == search_for_rate].iloc[0]
        rate_mid = int(rate_movie_row['movieId'])

        stars = st.select_slider(
            "Your Rating:",
            options=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
            value=st.session_state.user_ratings.get(rate_mid, 4.5)
        )
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("💾 Save Rating", use_container_width=True):
                st.session_state.user_ratings[rate_mid] = float(stars)
                st.toast(f"Saved {stars}★ for {rate_movie_row['clean_title']}!", icon="✅")
                st.rerun()
        with btn_c2:
            if rate_mid in st.session_state.user_ratings:
                if st.button("🗑️ Remove Rating", use_container_width=True):
                    del st.session_state.user_ratings[rate_mid]
                    st.toast(f"Removed {rate_movie_row['clean_title']}.", icon="ℹ️")
                    st.rerun()

    with r_col2:
        st.subheader("Profile Stats")
        total_r = len(st.session_state.user_ratings)
        avg_r = np.mean(list(st.session_state.user_ratings.values())) if total_r > 0 else 0.0
        
        st.markdown(
            f"<div class='stat-card-box' style='margin-bottom:12px;'><div class='stat-icon-circle'>⭐</div><div><div class='stat-number'>{total_r}</div><div class='stat-label-text'>Movies Rated</div></div></div>"
            f"<div class='stat-card-box'><div class='stat-icon-circle'>🎯</div><div><div class='stat-number'>{avg_r:.1f} ★</div><div class='stat-label-text'>Average Rating Given</div></div></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("Your Rated Movies")

    if st.session_state.user_ratings:
        user_rated_rows = []
        for mid, r in st.session_state.user_ratings.items():
            m_info = movies_df[movies_df['movieId'] == mid]
            if not m_info.empty:
                row = m_info.iloc[0].to_dict()
                row['my_rating'] = r
                user_rated_rows.append(row)

        user_rated_df = pd.DataFrame(user_rated_rows)
        display_df = user_rated_df[['clean_title', 'year', 'genres_str', 'my_rating', 'avg_rating']].rename(columns={
            'clean_title': 'Movie Title',
            'year': 'Year',
            'genres_str': 'Genres',
            'my_rating': 'Your Rating (★)',
            'avg_rating': 'Community Avg (★)'
        })
        st.dataframe(display_df, use_container_width=True)

        if st.button("🚀 View Recommendations For Me"):
            st.session_state.active_tab = "Recommendations"
            st.rerun()
    else:
        st.info("You haven't rated any movies yet. Select a movie above to add your first rating!")

# ==========================================
# 6. MOVIE DETAILS
# ==========================================
elif st.session_state.active_tab == "Movie Details":
    mid = st.session_state.selected_movie_id
    movie_info = movies_df[movies_df['movieId'] == mid]
    remote_movie = st.session_state.get("selected_remote_movie")
    
    if movie_info.empty and (
        not remote_movie or int(remote_movie.get("movieId", -1)) != int(mid)
    ):
        st.warning("Movie not found.")
    elif movie_info.empty:
        title = remote_movie.get("clean_title", remote_movie.get("title", "Movie"))
        year = remote_movie.get("year")
        details = get_movie_metadata(
            int(remote_movie["tmdbId"]), title, year,
        )
        st.image(details.get("poster_path"), width=320)
        st.title(f"{title} ({year})" if year else title)
        st.write(
            f"TMDB rating: {details.get('vote_average', 'N/A')}/10 · "
            f"Runtime: {details.get('runtime') or 'Not available'} minutes"
        )
        st.write(details.get("overview", "No synopsis is available."))
        info_rows = [
            ("Genres", ", ".join(details.get("genres", [])) or "N/A"),
            ("IMDb rating", details.get("imdb_rating") or "N/A"),
            ("IMDb votes", details.get("imdb_votes") or "N/A"),
            ("Director", details.get("director") or "N/A"),
            ("Cast", details.get("actors") or "N/A"),
            ("Awards", details.get("awards") or "N/A"),
            ("Language", details.get("language") or "N/A"),
            ("Country", details.get("country") or "N/A"),
        ]
        st.table(pd.DataFrame(info_rows, columns=["Field", "Value"]))
        if details.get("trailer_url"):
            st.link_button("▶️ Watch Official Trailer", details["trailer_url"])
    else:
        movie = movie_info.iloc[0]
        title = movie['clean_title']
        raw_year = movie['year']
        year_str = str(int(raw_year)) if raw_year and not pd.isna(raw_year) else "N/A"
        genres = movie['genres_str']
        avg_rating = movie['avg_rating']
        v_count = movie['rating_count']
        tmdb_id = int(movie.get('tmdbId', 0))

        details = get_movie_metadata(tmdb_id, title, raw_year)

        d_col1, d_col2 = st.columns([1, 2])
        with d_col1:
            st.image(details.get('poster_path'), use_container_width=True)
            if details.get('trailer_url'):
                st.link_button("▶️ Watch Official Trailer", details.get('trailer_url'), use_container_width=True)

        with d_col2:
            st.markdown(f"# {title} <span style='font-size:1.5rem; color:#94a3b8;'>({year_str})</span>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='display:flex; gap:12px; align-items:center; margin-bottom:15px;'>"
                f"<span style='background:#1e3a8a; color:#60a5fa; padding:4px 10px; border-radius:6px; font-weight:700;'>★ {avg_rating:.1f} / 5.0</span>"
                f"<span style='color:#94a3b8; font-size:0.9rem;'>({v_count:,} Ratings)</span>"
                f"<span style='color:#cbd5e1; font-size:0.9rem;'>• {genres}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            st.subheader("Overview")
            st.write(details.get('overview'))

            meta_data = {
                "Field": [
                    "Release Date", "Runtime", "TMDB Rating", "IMDb Rating",
                    "IMDb Votes", "Director", "Cast", "Genres", "Catalog ID",
                ],
                "Value": [
                    details.get('released') or details.get('release_date', 'N/A'),
                    f"{details.get('runtime')} minutes" if details.get('runtime') else "N/A",
                    f"{details.get('vote_average', 7.5)}/10",
                    details.get("imdb_rating") or "N/A",
                    details.get("imdb_votes") or "N/A",
                    details.get("director") or "N/A",
                    details.get("actors") or "N/A",
                    genres, str(mid),
                ]
            }
            st.table(pd.DataFrame(meta_data))

            curr_rating = st.session_state.user_ratings.get(mid, 4.0)
            st.write("Rate this title:")
            col_rate, col_submit = st.columns([2, 1])
            with col_rate:
                user_star = st.slider("Rating", 0.5, 5.0, float(curr_rating), 0.5, key="detail_star")
            with col_submit:
                if st.button("Save Rating", key="detail_save_btn", use_container_width=True):
                    st.session_state.user_ratings[mid] = user_star
                    st.toast(f"Saved {user_star}★ for {title}!", icon="⭐")

        st.markdown("---")
        st.subheader("🍿 Similar Movies")
        similar_movies = cb_model.recommend_by_movie_id(mid, top_n=6)
        if not similar_movies.empty:
            sim_cols = st.columns(6)
            for idx, (_, r) in enumerate(similar_movies.iterrows()):
                badge = f"{r.get('match_percentage', 80):.1f}% Sim"
                render_movie_card(r, score_badge=badge, col_obj=sim_cols[idx])

# ==========================================
# 7. ANALYTICS
# ==========================================
elif st.session_state.active_tab == "Analytics":
    st.title("📊 ML Performance & Evaluation Benchmark")
    st.markdown("Comparative experimental analysis between **Content-Based**, **Collaborative Filtering**, and **Hybrid** architectures.")

    eval_data = get_cached_or_default_metrics()
    hybrid_metrics = eval_data["hybrid"]
    collab_metrics = eval_data["collaborative"]

    st.markdown(
        "<div class='stats-grid'>"
        f"<div class='stat-card-box'><div class='stat-icon-circle'>🎯</div><div><div class='stat-number'>{hybrid_metrics['precision']:.1f}%</div><div class='stat-label-text'>Hybrid Precision@{eval_data['k']}</div></div></div>"
        f"<div class='stat-card-box'><div class='stat-icon-circle'>🔁</div><div><div class='stat-number'>{hybrid_metrics['recall']:.1f}%</div><div class='stat-label-text'>Hybrid Recall@{eval_data['k']}</div></div></div>"
        f"<div class='stat-card-box'><div class='stat-icon-circle'>🔥</div><div><div class='stat-number'>{hybrid_metrics['hit_rate']:.1f}%</div><div class='stat-label-text'>Hybrid Hit Rate@{eval_data['k']}</div></div></div>"
        f"<div class='stat-card-box'><div class='stat-icon-circle'>📉</div><div><div class='stat-number'>{collab_metrics['rmse'] if collab_metrics['rmse'] is not None else 'N/A'}</div><div class='stat-label-text'>Collaborative RMSE</div></div></div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.subheader("📈 Algorithm Benchmark Comparison")
    chart_df = pd.DataFrame({
        "Algorithm": ["Content-Based Filtering", "Collaborative Filtering", "Hybrid Fusion (α=0.5)"],
        f"Precision@{eval_data['k']} (%)": [
            eval_data["content_based"]["precision"], collab_metrics["precision"],
            hybrid_metrics["precision"],
        ],
        f"Recall@{eval_data['k']} (%)": [
            eval_data["content_based"]["recall"], collab_metrics["recall"],
            hybrid_metrics["recall"],
        ],
        f"Hit Rate@{eval_data['k']} (%)": [
            eval_data["content_based"]["hit_rate"], collab_metrics["hit_rate"],
            hybrid_metrics["hit_rate"],
        ],
    }).set_index("Algorithm")

    st.bar_chart(chart_df, height=350)

    st.subheader("🔍 Architectural Tradeoff Matrix")
    comparison_table = pd.DataFrame([
        {
            "Dimension": "Core ML Mechanism",
            "Content-Based": "TF-IDF Vectorization + Cosine Similarity",
            "Collaborative Filtering": "User-Item Matrix + Pearson/Cosine",
            "Hybrid Fusion": "Linear Score Fusion (α·S_CB + (1-α)·S_CF)"
        },
        {
            "Dimension": "Item Cold Start (New Movie)",
            "Content-Based": "✅ Excellent (Uses metadata instantly)",
            "Collaborative Filtering": "❌ Poor (Requires crowd ratings)",
            "Hybrid Fusion": "✅ Robust (Falls back to Content signals)"
        },
        {
            "Dimension": "User Cold Start (New User)",
            "Content-Based": "✅ Instant (Needs just 1 liked movie)",
            "Collaborative Filtering": "❌ Poor (Requires user rating history)",
            "Hybrid Fusion": "✅ Robust (Smooth transition as ratings grow)"
        },
        {
            "Dimension": "Serendipity / Discovery",
            "Content-Based": "⚠️ Low (Overspecializes in same genre)",
            "Collaborative Filtering": "✅ High (Finds surprising cross-genre hits)",
            "Hybrid Fusion": "✅ Optimal (Maintains relevance & surprise)"
        }
    ])
    st.dataframe(comparison_table, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Dataset Statistics & Genre Distribution")
    g_col1, g_col2 = st.columns([1, 1])
    with g_col1:
        st.markdown(
            "<div style='background:#0e1424; padding:20px; border-radius:12px; border:1px solid #1a233a; line-height:2;'>"
            "<h4 style='color:#00d2ff; margin-top:0;'>MovieLens 100k Benchmark</h4>"
            "• <b>Total Catalog Movies:</b> 9,742<br>"
            "• <b>Total Ratings Recorded:</b> 100,836<br>"
            "• <b>Total Distinct Users:</b> 610<br>"
            "• <b>Rating Matrix Sparsity:</b> 98.3%<br>"
            "• <b>User-generated Tags:</b> 3,683<br>"
            "• <b>Rating Scale:</b> 0.5 to 5.0 (0.5 star increments)"
            "</div>",
            unsafe_allow_html=True
        )
    with g_col2:
        all_genres_flattened = [g for sublist in movies_df['genres_list'] for g in sublist if g != 'Unknown']
        genre_counts = pd.Series(all_genres_flattened).value_counts().head(8)
        st.write("Top 8 Genres in Catalog:")
        st.bar_chart(genre_counts)

# ==========================================
# 8. ABOUT
# ==========================================
elif st.session_state.active_tab == "About":
    st.title("ℹ️ About MovieMind AI")
    st.markdown(
        """
        **MovieMind AI** is a state-of-the-art hybrid recommendation system engineered with Machine Learning in Python.
        
        ### Architecture Highlights
        - **Content-Based Filtering**: TF-IDF vectorization over movie titles, genres, and user tags + Cosine distance ranking.
        - **Collaborative Filtering**: Mean-centered User-Item interaction matrix calculating Pearson/Cosine similarities between user taste profiles.
        - **Weighted Hybrid Fusion**: Dynamic score interpolation ($Score_{Hybrid} = \\alpha S_{CB} + (1-\\alpha) S_{CF}$), with fallbacks when a signal is unavailable.
        - **Live Catalog**: TMDB discovery for current releases and OMDb metadata by IMDb ID; live titles are not added to MovieLens-trained models.
        
        *Engineered with Streamlit, Scikit-Learn, Pandas, and TMDB API.*
        """
    )

# ==========================================
# 9. SETTINGS
# ==========================================
elif st.session_state.active_tab == "Settings":
    st.title("⚙️ System Settings & API")
    st.markdown("Configure your external The Movie Database (TMDB) API credentials.")

    st.subheader("TMDB API Connection")
    current_key = tmdb_client.api_key
    new_key = st.text_input("TMDB API Key (v3 auth)", value=current_key, type="password")

    c_save, c_test = st.columns(2)
    with c_save:
        if st.button("💾 Save Key", use_container_width=True):
            tmdb_client.set_api_key(new_key)
            save_env_value("TMDB_API_KEY", new_key.strip())
            st.success("API Key updated and saved!")
            st.rerun()

    with c_test:
        if st.button("🧪 Test Connection", use_container_width=True):
            if not new_key:
                st.warning("Please enter an API Key.")
            else:
                try:
                    import requests
                    test_url = f"https://api.tmdb.org/3/movie/550?api_key={new_key.strip()}"
                    r = requests.get(test_url, timeout=5)
                    if r.status_code == 200:
                        data = r.json()
                        st.success(f"Connected! Verified with: '{data.get('title')}'")
                    else:
                        st.error(f"Failed to authenticate: HTTP {r.status_code}")
                except Exception as e:
                    st.error(f"Error testing connection: {e}")

    st.markdown("---")
    st.subheader("OMDb Movie Details")
    st.caption(
        "OMDb supplies IMDb-linked runtime, plot, cast and rating details. "
        "Set OMDB_API_KEY in your local .env; do not commit that file."
    )
    omdb_key = st.text_input(
        "OMDb API Key", value=omdb_client.api_key, type="password"
    )
    omdb_save, omdb_test = st.columns(2)
    with omdb_save:
        if st.button("💾 Save OMDb Key", use_container_width=True):
            omdb_client.set_api_key(omdb_key)
            save_env_value("OMDB_API_KEY", omdb_key.strip())
            st.success("OMDb key saved locally.")
            st.rerun()
    with omdb_test:
        if st.button("🧪 Test OMDb Connection", use_container_width=True):
            if not omdb_key:
                st.warning("Add a rotated OMDb key first.")
            else:
                try:
                    omdb_client.set_api_key(omdb_key)
                    test_details = omdb_client.get_movie_details(
                        imdb_id="tt3896198"
                    )
                    if test_details:
                        st.success("OMDb connected and returned movie details.")
                    else:
                        st.error("OMDb returned no matching movie.")
                except requests.RequestException as error:
                    st.error(f"OMDb connection failed: {error}")

    st.markdown("---")
    st.subheader("Cache Management")
    if st.button("🧹 Clear Poster & Metadata Cache"):
        cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'tmdb_cache.json')
        if os.path.exists(cache_path):
            os.remove(cache_path)
            tmdb_client.cache = {}
            st.success("Cache cleared!")
        else:
            st.info("Cache is empty.")
