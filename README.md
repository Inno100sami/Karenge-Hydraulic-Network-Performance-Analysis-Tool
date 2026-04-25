# 💧 Karenge Water Supply Network – Hydraulic Model Dashboard

[![Live Dashboard](https://inno100sami.github.io/Karenge-Hydraulic-Network-Performance-Analysis-Tool/karenge-dashboard.html)
---

## 📖 About This Project

This repository hosts an interactive **HTML dashboard** summarising the EPANET hydraulic model of the **Karenge Water Supply Network** operated by the **Water and Sanitation Corporation (WASAC) – Rwamagana Branch**, Rwanda.

The model was developed under the **SCALE Project** (Scaling Climate-Adaptive WASH) and built using **GIS** for network mapping and **EPANET** for hydraulic modelling. The dashboard presents key network statistics, pressure zone analysis, pump performance, storage tank inventory, demand patterns, and elevation data in a single, self-contained web page — no server or database required.

---

## 🗺️ Network Overview

| Parameter | Value |
|---|---|
| **Location** | Rwamagana District, Eastern Province, Rwanda |
| **Coordinate System** | UTM Zone 36S |
| **Elevation Range** | 1,357 m – 1,736 m ASL |
| **Source** | Karenge Water Treatment Plant (WTP) |
| **Simulation Period** | 24 hours (2020-07-23) |
| **Hydraulic Timestep** | 10 minutes (144 steps) |
| **Headloss Formula** | Hazen-Williams |
| **Model File** | `2020-Rwamagana-Karenge_Rev1.inp` |

---

## 📊 Dashboard Features

### KPI Summary Panel
At-a-glance figures for the entire network:
- 9,752 junctions | 9,796 pipe links
- 32 storage tanks | 11 pumps across 3 stations
- 43.8 L/s base demand | 59.9 L/s peak demand
- 340 m elevation range

### 🌡️ Pressure Zone Analysis *(new)*
Tanks and junctions are classified into **5 colour-coded pressure bands** based on estimated hydraulic head:

| Zone | Pressure Range | Colour | Interpretation |
|---|---|---|---|
| Very Low | 0 – 5 bar | 🔵 Blue | Pressure-deficient; may need booster |
| Normal | 6 – 15 bar | 🟢 Green | Within WHO / WASAC standard |
| High | 16 – 20 bar | 🟡 Amber | Monitor for leakage risk |
| Very High | 21 – 25 bar | 🔴 Red | PRV (pressure reducing valve) recommended |
| Critical | > 25 bar | 🟣 Purple | Pipe failure risk; immediate attention required |

Each zone card displays the **count of affected tanks**, estimated **node count**, and **average pressure**. A horizontal bar chart shows the **percentage share of network nodes** per zone. The **overall network average pressure** (weighted) is shown prominently at the top of this section.

### 🔽 Interactive Filters *(new)*
A persistent filter bar at the top of the page lets users slice the **tank inventory table** by:
- **Zone** – select any of the 14 supply zones (GAHKIB, KARBIC, KARNYA, NYABIH, etc.)
- **Pressure Zone** – filter by pressure band (Very Low → Critical)
- **Minimum Diameter** – show only tanks above a specified diameter (metres)
- **Minimum Elevation** – show only tanks above a specified elevation (metres ASL)

A live counter updates to show how many tanks match the current filter combination. A **Reset** button restores all tanks.

### 🗺️ Network Topology Schematic
Canvas-rendered schematic showing the flow path from the Karenge WTP source reservoir through pump stations to all service zones, with elevation contour lines.

### ⏱️ 24-Hour Demand Pattern
Line chart of the residential demand multiplier curve (Resid_profile) across all 144 ten-minute simulation timesteps, showing peak, base, and night-minimum demand.

### ⛰️ Elevation Distribution
Bar chart of the 9,752 junctions distributed across 7 elevation bands between 1,350 m and 1,700 m ASL.

### 🔩 Pipe Diameter Distribution
Horizontal bar chart and doughnut chart showing the split of 9,796 pipe links by diameter — dominated by Ø 25 mm service connections (67.4%).

### ⚙️ Pump Station Specifications
Cards for each of the 3 pump stations:
- Karenge-Rugara (3 pumps, H₀ = 200 m)
- Karenge-Nyabihu (7 pumps, H₀ up to 240 m)
- Gahuka Booster (1 pump, H₀ = 200 m)

Accompanied by interactive Q-H (flow vs. head) curves for all 5 pump types.

### 🏗️ Storage Tank Inventory
Filterable table of all 32 tanks with columns for zone, elevation, diameter, operating levels, **estimated pressure**, **pressure zone classification**, maximum usable storage volume, and mixing model.

### 🗂️ Simulation Parameters
Full reference table of model configuration: software source, flow units, H-W roughness coefficients, convergence tolerances, and coordinate system.

---

## 🚀 Viewing the Dashboard

### Option 1 — GitHub Pages (recommended)
If GitHub Pages is enabled for this repository, the site is live at:

```
https://<your-username>.github.io/<repo-name>/
```

The root URL serves `index.html`, which links to:
- `karenge-dashboard.html`
- `karenge-pressure-map.html`

### Option 2 — Download and open locally
1. Clone or download this repository
2. Open `index.html` (or `karenge-dashboard.html`) in any modern browser (Chrome, Firefox, Edge, Safari)
3. No installation, server, or internet connection required after download

### Option 3 — View raw file
Click **`karenge-dashboard.html`** in the file list above, then click **"Raw"** and save to your machine.

---

## 📁 Repository Structure

```
.
├── README.md                    ← This file
├── index.html                   ← GitHub Pages entry page
├── karenge-dashboard.html       ← Main interactive dashboard
├── karenge-pressure-map.html    ← Pressure zone satellite map
└── pipe_data.js                 ← Pipe geometry data for map/dashboard
```

---

## � Next Phase

The following analytical work is planned for the next development phase:

### 🔴 Leakage Integration into Pressure Zones
Field-mapped leakage points (burst pipes, illegal connections, and visible losses) will be geo-referenced and overlaid on the pressure zone map. Each leakage event will be tagged to its corresponding pressure band (0–5 bar up to >25 bar) to test the hypothesis that **high-pressure zones (>16 bar) generate disproportionately more leakage** — a key input for prioritising pressure management interventions such as PRVs and pipe replacement.

### 🔬 Deep Network Analysis
Building on the EPANET model, the next phase will include:
- **Velocity & headloss analysis** — identifying pipes with sub-optimal velocities (<0.3 m/s stagnation risk or >2.0 m/s erosion risk) and high unit headloss corridors
- **Demand deficit mapping** — locating nodes where residual pressure falls below the WHO/WASAC minimum of 0.5 bar during peak demand hours
- **Storage adequacy review** — comparing tank volumes against zone demand and assessing whether storage duration meets the target of 12–24 hours
- **Network resilience scenarios** — pipe failure and pump-out-of-service simulations to quantify impact on supply continuity
- **Non-Revenue Water (NRW) estimation** — correlating modelled leakage proxies (high pressure zones, pipe age, material) with real-world NRW data from WASAC billing records

---

## �🛠️ Technology

The dashboard is a **single self-contained HTML file** with no build step or backend dependency:

- **HTML5 / CSS3** — layout, responsive grid, animations
- **Vanilla JavaScript** — filter logic, table rendering, canvas drawing
- **[Chart.js 4.4.1](https://www.chartjs.org/)** (CDN) — demand pattern, elevation, pipe diameter, and pump curve charts
- **HTML Canvas API** — network topology schematic

---

## 🏛️ Data Sources & Disclaimer

All hydraulic data is derived from the **EPANET model file** `2020-Rwamagana-Karenge_Rev1.inp`, produced by WASAC Rwamagana Branch under the SCALE Project (model date: 23 July 2020).

**Pressure estimates** shown in the dashboard are calculated from tank elevation, initial water level, and pump head data. They represent **design/modelled pressures** under the simulated 24-hour pattern and should not be treated as real-time operational readings.

---

## 👥 Credits

| Role | Organisation |
|---|---|
| Network Owner & Operator | WASAC – Rwamagana Branch, Rwanda |
| Project Framework | SCALE Project |
| Model Software | GIS + EPANET |
| Dashboard Development | April 2026 |

---

## 📄 Licence

This dashboard is shared for **informational and capacity-building purposes** within the SCALE Project. For reuse or redistribution of the underlying hydraulic model data, please contact WASAC Rwamagana Branch directly.

---

*Dashboard last updated: April 2026*
