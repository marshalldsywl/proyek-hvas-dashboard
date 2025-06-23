import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.font_manager as fm # Ditambahkan untuk manajemen font

# --- Konfigurasi Halaman dan CSS Kustom ---
st.set_page_config(layout="wide", page_title="Dashboard Progres HVAS", page_icon="✨")

css_content = """
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Orbitron:wght@400;700&display=swap');

body {
    font-family: 'Roboto', sans-serif;
    color: #E0E0E0;
    background-color: #0A0F18;
}

h1 { /* Judul utama dashboard */
    font-family: 'Orbitron', sans-serif !important;
    color: #00DFFC !important;
    text-shadow:
        0 0 5px rgba(0, 223, 252, 1),
        0 0 10px rgba(0, 223, 252, 0.9),
        0 0 20px rgba(0, 223, 252, 0.7),
        0 0 35px rgba(0, 223, 252, 0.5),
        0 0 50px rgba(0, 223, 252, 0.3);
}

h2, h3 { /* Gaya untuk "Ringkasan Progres Proyek HVAS" */
    font-family: 'Orbitron', sans-serif;
    font-size: 1.2em;
    color: #C399FF; /* Ungu muda */
    border-bottom: 1px solid #C399FF;
    padding-bottom: 8px;
    margin-top: 20px;
    flexdirection: column;
    justify-content: center;
}

/* Penyesuaian untuk Kartu Metrik agar terlihat seperti sel grid futuristik */
div[data-testid="stMetric"] {
    background-color: #161B22; /* Latar belakang kartu sedikit lebih gelap */
    border-radius: 10px; /* Radius sudut kartu */
    padding: 20px 25px; /* Padding di dalam kartu */
    box-shadow: 0 0 15px rgba(0, 223, 252, 0.2), inset 0 0 5px rgba(0, 223, 252, 0.1); /* Bayangan luar dan sedikit ke dalam */
    border: 1.5px solid #00AACC; /* Border kartu lebih tegas */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%; /* Membuat kartu mengisi tinggi kolomnya jika dalam st.columns */
    display: flex; /* Memungkinkan penataan konten di dalam kartu */
    flex-direction: column; /* Konten (label & nilai) ditata secara vertikal */
    justify-content: center; /* Pusatkan konten secara vertikal jika ada ruang lebih */
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-5px) scale(1.02); /* Efek hover sedikit terangkat dan membesar */
    box-shadow: 0 0 25px rgba(0, 223, 252, 0.3), inset 0 0 8px rgba(0, 223, 252, 0.2);
}

/* Label Metrik: Gaya disamakan dengan H2 (Orbitron, Ungu Muda) */
label[data-testid="stMetricLabel"],
label[data-testid="stMetricLabel"] div,
label[data-testid="stMetricLabel"] p,
label[data-testid="stMetricLabel"] span {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    color: #C399FF !important; /* Warna ungu muda */
    font-size: 1em !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin: 8px 0 8px 0 !important; /* margin-bottom untuk jarak ke nilai */
    padding: 0 !important;
    line-height: 1.2 !important;
    text-shadow: none !important; /* Pastikan tidak ada glow */
    background-color: transparent !important;
    text-align: center; /* Label di tengah kartu */
}
label[data-testid="stMetricLabel"] { /* Kontainer label itu sendiri */
    display: block !important;
}


/* Nilai Metrik (Orbitron, Cyan, Glow) */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] div,
div[data-testid="stMetricValue"] p,
div[data-testid="stMetricValue"] span {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2em !important;
    color: #00DFFC !important; /* Warna Cyan */
    font-weight: 700 !important;
    line-height: 1.0 !important;
    background-color: transparent !important;
    margin: 0 !important;
    padding: 0 !important;
    text-align: center; /* Nilai di tengah kartu */
}
div[data-testid="stMetricValue"] { /* Kontainer nilai itu sendiri */
    display: block !important;
    padding-top: 5px !important; /* Sedikit padding atas untuk nilai */
}


hr {
    border-top: 1px solid #C399FF;
    margin-top: 25px;
    margin-bottom: 25px;
}

div[data-testid="stAlert"] {
    border-radius: 8px;
    font-family: 'Roboto', sans-serif;
    border-width: 1px;
    padding: 12px 15px;
    font-size: 1.0rem;
}
div[data-testid="stAlert"][data-baseweb="alert"][role="alert"] { /* Warning */
    background-color: rgba(255, 176, 0, 0.1);
    border-color: #FFB000;
}
div[data-testid="stAlert"][data-baseweb="alert"][role="alert"] > div:nth-child(2) {
    color: #FFD371;
}
div[data-testid="stAlert"][data-baseweb="alert"][role="status"] { /* Success */
    background-color: rgba(20, 204, 140, 0.1);
    border-color: #14CC8C;
}
div[data-testid="stAlert"][data-baseweb="alert"][role="status"] > div:nth-child(2) {
    color: #6EFFCA;
}
div[data-testid="stAlert"][data-baseweb="alert"] > div:first-child svg { /* Error icon */
    fill: #FF6B6B;
}
div[data-testid="stAlert"][data-baseweb="alert"] > div:nth-child(2) { /* Error text */
    color: #FF8F8F !important;
}

.stPlotlyChart, .stMatplotlibChart { /* Kontainer grafik */
    background-color: #161B22;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0, 223, 252, 0.1);
    border: 1px solid #007ACC;
}
.stMatplotlibChart > div > img { /* Gambar plot di dalam kontainer */
    border-radius: 8px;
}
"""
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# --- Memuat Font Kustom untuk Matplotlib (Tanpa Notifikasi Sidebar) ---
orbitron_font_path = 'Orbitron-Bold.ttf' # Sesuaikan jika nama file atau path berbeda
roboto_font_path = 'Roboto-Regular.ttf'   # Sesuaikan jika nama file atau path berbeda

prop_orbitron_title = None
prop_roboto_label = None

if os.path.exists(orbitron_font_path) and os.path.exists(roboto_font_path):
    try:
        prop_orbitron_title = fm.FontProperties(fname=orbitron_font_path)
        prop_roboto_label = fm.FontProperties(fname=roboto_font_path)
    except RuntimeError:
        pass # Abaikan error jika font rusak, akan fallback ke default
else:
    pass # Abaikan jika file tidak ditemukan, akan fallback ke default

# Judul Utama Dashboard
st.markdown(
    "<h1 style='text-align: center;'>Dashboard Progres HVAS</h1>",
    unsafe_allow_html=True
)

# --- Logika Pencarian File dan Pengolahan Data ---
csv_filename = None
search_dirs = ["."]
if os.path.exists("data") and os.path.isdir("data"):
    search_dirs.append("data")

for s_dir in search_dirs:
    try:
        for file in os.listdir(s_dir):
            if file.endswith(".csv") and "mvp" in file.lower():
                csv_filename = os.path.join(s_dir, file)
                break
    except FileNotFoundError:
        continue
    if csv_filename:
        break

if csv_filename is None:
    st.error("❌ Tidak ditemukan file CSV yang mengandung kata 'mvp' di nama file (di direktori saat ini atau './data/').")
else:
    # st.success(f"✅ File ditemukan: {os.path.basename(csv_filename)}") # Menampilkan nama file saja

    try:
        df_input = pd.read_csv(csv_filename)

        if 'Minggu' not in df_input.columns or 'Total Sisa SP' not in df_input.columns:
            st.error("❌ File CSV harus memiliki kolom: `Minggu` dan `Total Sisa SP`")
        else:
            df_input['Minggu'] = pd.to_numeric(df_input['Minggu'], errors='coerce').fillna(0).astype(int)
            df_input = df_input[df_input['Minggu'] > 0]
            df_input = df_input.sort_values(by='Minggu').reset_index(drop=True)
            
            if df_input.empty:
                 st.warning("⚠️ Data minggu tidak valid atau kosong setelah pembersihan dalam file CSV.")
            else:
                max_week_in_data = df_input['Minggu'].max()
                
                full_weeks_df = pd.DataFrame({'Minggu': list(range(1, max_week_in_data + 1))})
                df_processed = pd.merge(full_weeks_df, df_input, on='Minggu', how='left')

                df_processed['Total Sisa SP'] = pd.to_numeric(df_processed['Total Sisa SP'], errors='coerce')
                df_non_null = df_processed.dropna(subset=['Total Sisa SP'])

                if df_non_null.empty:
                    st.error("❌ Tidak ada data 'Total Sisa SP' yang valid (numerik) setelah diproses.")
                else:
                    minggu_plot_aktual = df_processed['Minggu']
                    sp_remaining_plot_aktual = df_processed['Total Sisa SP']

                    total_sp_at_start = float(df_non_null['Total Sisa SP'].iloc[0])
                    current_last_week_with_data = int(df_non_null['Minggu'].iloc[-1])
                    current_sp_remaining = float(df_non_null['Total Sisa SP'].iloc[-1])
                    
                    sp_completed = total_sp_at_start - current_sp_remaining
                    percentage_completed = (sp_completed / total_sp_at_start) * 100 if total_sp_at_start > 0 else 0

                    ideal_burndown_values_plot = []
                    if max_week_in_data > 1:
                        ideal_burndown_values_plot = [total_sp_at_start - (total_sp_at_start / (max_week_in_data - 1)) * i for i in range(max_week_in_data)]
                    elif max_week_in_data == 1:
                        ideal_burndown_values_plot = [total_sp_at_start]
                    
                    minggu_plot_ideal = list(range(1, max_week_in_data + 1))

                    weeks_remaining_target = max_week_in_data - current_last_week_with_data
                    recommendation_sp_per_week = 0
                    if weeks_remaining_target > 0 and current_sp_remaining > 0:
                        recommendation_sp_per_week = current_sp_remaining / weeks_remaining_target

                    # --- PENEMPATAN METRIK DALAM GRID 2x2 ---
                    st.markdown("## ")

                    # Baris pertama grid
                    row1_col1, row1_col2 = st.columns(2, gap="medium") # Anda bisa ganti "medium" dengan "small" atau "large"
                    with row1_col1:
                        st.metric("📦 Total Pekerjaan", f"{int(total_sp_at_start)}")
                    with row1_col2:
                        st.metric("✅ Pekerjaan Selesai", f"{int(sp_completed)}")

                    # Baris kedua grid
                    row2_col1, row2_col2 = st.columns(2, gap="medium") # Anda bisa ganti "medium" dengan "small" atau "large"
                    with row2_col1:
                        st.metric("⏳ Pekerjaan Tersisa", f"{int(current_sp_remaining)}")
                    with row2_col2:
                        st.metric("📈 Progres Aktual", f"{percentage_completed:.1f}%")
                    # --- AKHIR PENEMPATAN METRIK DALAM GRID 2x2 ---

                    st.markdown("---")

                    st.markdown("### 📉 Grafik Burndown")
                    fig, ax = plt.subplots(figsize=(12, 6))

                    actual_color = '#00DFFC'
                    ideal_color = '#FF6AC1'
                    grid_color = '#2A2F45'
                    text_color_plot = '#E0E0E0'
                    plot_bg_color = '#0A0F18'

                    fig.patch.set_alpha(0.0)
                    ax.set_facecolor(plot_bg_color)

                    ax.plot(minggu_plot_aktual, sp_remaining_plot_aktual, marker='o', linestyle='-', linewidth=2.5, markersize=8, label='Aktual', color=actual_color, mec=plot_bg_color, mew=1)
                    
                    if ideal_burndown_values_plot and len(ideal_burndown_values_plot) == len(minggu_plot_ideal):
                        ax.plot(minggu_plot_ideal, ideal_burndown_values_plot, linestyle='--', linewidth=2, label='Ideal', color=ideal_color, alpha=0.8)
                    elif max_week_in_data == 1 and total_sp_at_start > 0:
                         ax.plot([1, 1.99], [total_sp_at_start, 0], linestyle='--', linewidth=2, label='Ideal', color=ideal_color, alpha=0.8)


                    dynamic_xlabel = f"Saat ini proyek memasuki minggu ke {current_last_week_with_data} pelaksanaan."
                         
                    ax.set_xlabel(
                        dynamic_xlabel,
                        color=text_color_plot,
                        fontsize=14,
                        fontproperties=prop_roboto_label if prop_roboto_label else None,
                        labelpad=15
                    )
                    ax.set_ylabel(
                        'Pekerjaan Tersisa',
                        color=text_color_plot,
                        fontsize=14,
                        fontproperties=prop_roboto_label if prop_roboto_label else None
                    )

                    x_tick_positions = list(range(1, max_week_in_data + 1))
                    ax.set_xticks(x_tick_positions)
                    ax.set_xlim(0.5, max_week_in_data + 0.5)

                    ax.set_ylim(total_sp_at_start * 1.05 if total_sp_at_start > 0 else 10, 0)
                    
                    y_ticks_list_temp = [*list(range(0, int(total_sp_at_start) + 1, 20)), int(total_sp_at_start)]
                    y_ticks_list = sorted(list(set(y_ticks_list_temp)))
                    if not y_ticks_list:
                        y_ticks_list = [0, int(total_sp_at_start)] if total_sp_at_start > 0 else [0,1]
                    ax.set_yticks(y_ticks_list)
                    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))

                    ax.tick_params(axis='x', colors=text_color_plot, labelcolor=text_color_plot, labelsize=11)
                    ax.tick_params(axis='y', colors=text_color_plot, labelcolor=text_color_plot, labelsize=10)
                    
                    for spine in ax.spines.values():
                        spine.set_edgecolor(grid_color)
                    ax.grid(True, color=grid_color, linestyle=':', linewidth=0.7, alpha=0.7)
                    legend = ax.legend(facecolor=plot_bg_color, edgecolor=ideal_color, labelcolor=text_color_plot, fontsize=10, loc='upper left')
                    for text_leg in legend.get_texts():
                        text_leg.set_color(text_color_plot)


                    st.pyplot(fig, use_container_width=True)
                    st.markdown("---")

                    if current_sp_remaining <= 0:
                        if current_last_week_with_data <= max_week_in_data:
                             st.success("🎉 Selamat! Semua Story Points telah selesai dikerjakan tepat waktu atau lebih awal.")
                        else:
                             st.success(f"🎉 Selamat! Semua Story Points telah selesai dikerjakan (pada minggu ke-{current_last_week_with_data}).")
                    elif weeks_remaining_target > 0:
                        st.warning(f"📈 **Rekomendasi:** Untuk dapat menyelesaikan dengan tepat waktu ({max_week_in_data} minggu), selesaikan sekitar **{recommendation_sp_per_week:.1f} Pekerjaan/minggu** selama {weeks_remaining_target} minggu tersisa.")
                    elif weeks_remaining_target == 0 and current_sp_remaining > 0:
                        st.error(f"🚨 **Perhatian:** Anda berada di minggu terakhir target data ({max_week_in_data}) namun masih ada {int(current_sp_remaining)} SP tersisa.")
                    else:
                        st.error(f"🚨 **Perhatian:** Proyek telah melewati target minggu terakhir data ({max_week_in_data}) dan masih ada {int(current_sp_remaining)} SP tersisa.")

    except FileNotFoundError:
        st.error(f"❌ File CSV tidak ditemukan pada path: `{csv_filename}`. Pastikan file ada di lokasi yang benar.")
    except pd.errors.EmptyDataError:
        st.error(f"❌ File CSV `{csv_filename}` kosong atau tidak memiliki header yang benar.")
    except ValueError as ve:
        st.error(f"❌ Terjadi kesalahan nilai saat memproses data: {ve}. Periksa format angka di kolom 'Minggu' atau 'Total Sisa SP'.")
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan umum saat memproses file: {e}")
        # st.exception(e)http://192.168.68.65:8501/