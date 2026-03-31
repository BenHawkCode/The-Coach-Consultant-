#!/usr/bin/env node
/**
 * Generate portrait story asset HTML files from manifest.
 * Each asset is 1080x1920 with one of 4 rotating background schemes.
 */

const fs = require('fs');
const path = require('path');

const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'story-asset-manifest.json'), 'utf8'));
const assetsDir = path.join(__dirname, 'assets');
if (!fs.existsSync(assetsDir)) fs.mkdirSync(assetsDir, { recursive: true });

// Icon base path (absolute for file:// rendering)
const ICON_BASE = path.resolve(__dirname, '..', 'Interactive Assets copy', 'exported-icons', 'png');

/* ─── BACKGROUND SCHEMES ─── */
const BG = {
  dark: {
    background: 'linear-gradient(135deg, #0a0a0a 0%, #1a2a2a 100%)',
    text: '#ffffff',
    textSecondary: '#aaaaaa',
    accent: '#7abfbf',
    accent2: '#FF6B35',
    cardBg: 'rgba(255,255,255,0.04)',
    cardBorder: 'rgba(255,255,255,0.08)',
    barBg: 'rgba(255,255,255,0.08)',
    barFill: '#5B9A9A',
    metricGradient: 'linear-gradient(135deg, #7abfbf, #FF6B35)',
    stepCircleBg: 'rgba(91,154,154,0.25)',
    stepCircleBorder: 'rgba(91,154,154,0.5)',
    stepCircleText: '#7abfbf',
    tagBg: 'rgba(91,154,154,0.15)',
    tagText: '#7abfbf',
    funnelColors: ['#5B9A9A', '#4d8a8a', '#3d7a7a', '#FF6B35', '#e55a2a'],
    checkColor: '#44ff88',
    crossColor: '#ff4444',
    iconFilter: 'none'
  },
  white: {
    background: '#FFFFFF',
    text: '#1A1A1A',
    textSecondary: '#777777',
    accent: '#5B9A9A',
    accent2: '#FF6B35',
    cardBg: '#F5F5F5',
    cardBorder: '#E0E0E0',
    barBg: '#E0E0E0',
    barFill: '#5B9A9A',
    metricGradient: 'linear-gradient(135deg, #5B9A9A, #FF6B35)',
    stepCircleBg: '#5B9A9A',
    stepCircleBorder: '#5B9A9A',
    stepCircleText: '#ffffff',
    tagBg: 'rgba(91,154,154,0.12)',
    tagText: '#5B9A9A',
    funnelColors: ['#5B9A9A', '#4d8a8a', '#3d7a7a', '#FF6B35', '#e55a2a'],
    checkColor: '#22aa55',
    crossColor: '#dd3333',
    iconFilter: 'none'
  },
  'teal-black': {
    background: 'linear-gradient(135deg, #0f2a2a 0%, #0a0a0a 100%)',
    text: '#ffffff',
    textSecondary: '#8abfbf',
    accent: '#7abfbf',
    accent2: '#FFD166',
    cardBg: 'rgba(91,154,154,0.12)',
    cardBorder: 'rgba(91,154,154,0.3)',
    barBg: 'rgba(91,154,154,0.15)',
    barFill: '#7abfbf',
    metricGradient: 'linear-gradient(135deg, #7abfbf, #FFD166)',
    stepCircleBg: 'rgba(91,154,154,0.3)',
    stepCircleBorder: 'rgba(91,154,154,0.6)',
    stepCircleText: '#7abfbf',
    tagBg: 'rgba(91,154,154,0.2)',
    tagText: '#7abfbf',
    funnelColors: ['#7abfbf', '#5B9A9A', '#3d7a7a', '#FFD166', '#FF6B35'],
    checkColor: '#44ff88',
    crossColor: '#ff4444',
    iconFilter: 'none'
  },
  teal: {
    background: 'linear-gradient(135deg, #5B9A9A 0%, #3d7a7a 100%)',
    text: '#ffffff',
    textSecondary: 'rgba(255,255,255,0.75)',
    accent: '#ffffff',
    accent2: '#FFD166',
    cardBg: 'rgba(255,255,255,0.12)',
    cardBorder: 'rgba(255,255,255,0.2)',
    barBg: 'rgba(255,255,255,0.15)',
    barFill: '#ffffff',
    metricGradient: 'linear-gradient(135deg, #ffffff, #FFD166)',
    stepCircleBg: 'rgba(255,255,255,0.2)',
    stepCircleBorder: 'rgba(255,255,255,0.4)',
    stepCircleText: '#ffffff',
    tagBg: 'rgba(255,255,255,0.15)',
    tagText: '#ffffff',
    funnelColors: ['#ffffff', 'rgba(255,255,255,0.8)', 'rgba(255,255,255,0.6)', '#FFD166', '#FF6B35'],
    checkColor: '#ffffff',
    crossColor: '#FFD166',
    iconFilter: 'none'
  },
  'orange-black': {
    background: 'linear-gradient(135deg, #FF6B35 0%, #1a0a00 65%, #0a0a0a 100%)',
    text: '#ffffff',
    textSecondary: 'rgba(255,255,255,0.8)',
    accent: '#ffffff',
    accent2: '#FFD166',
    cardBg: 'rgba(0,0,0,0.35)',
    cardBorder: 'rgba(255,255,255,0.15)',
    barBg: 'rgba(255,255,255,0.12)',
    barFill: '#ffffff',
    metricGradient: 'linear-gradient(135deg, #ffffff, #FFD166)',
    stepCircleBg: 'rgba(0,0,0,0.4)',
    stepCircleBorder: 'rgba(255,255,255,0.3)',
    stepCircleText: '#ffffff',
    tagBg: 'rgba(0,0,0,0.35)',
    tagText: '#ffffff',
    funnelColors: ['#ffffff', 'rgba(255,255,255,0.85)', 'rgba(255,255,255,0.7)', '#FFD166', '#1A1A1A'],
    checkColor: '#ffffff',
    crossColor: '#FFD166',
    iconFilter: 'none'
  }
};

/* ─── HTML TEMPLATE SHELL ─── */
function htmlShell(asset, theme, bodyContent) {
  const iconPath = `file://${path.join(ICON_BASE, asset.category, asset.icon)}`;
  const isWhite = asset.bg === 'white';

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  .story-asset {
    width: 1080px;
    height: 1920px;
    background: ${theme.background};
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 50px 44px;
    position: relative;
    overflow: hidden;
    font-family: 'Inter', sans-serif;
    color: ${theme.text};
  }

  /* Subtle background decoration */
  .story-asset::before {
    content: '';
    position: absolute;
    top: -200px; right: -200px;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: ${isWhite ? 'rgba(91,154,154,0.04)' : 'rgba(91,154,154,0.06)'};
    pointer-events: none;
  }
  .story-asset::after {
    content: '';
    position: absolute;
    bottom: -300px; left: -200px;
    width: 700px; height: 700px;
    border-radius: 50%;
    background: ${isWhite ? 'rgba(91,154,154,0.03)' : 'rgba(91,154,154,0.04)'};
    pointer-events: none;
  }

  .content-wrap {
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 28px;
  }

  .tag {
    display: inline-block;
    padding: 8px 24px;
    border-radius: 30px;
    font-size: 16px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    background: ${theme.tagBg};
    color: ${theme.tagText};
  }

  .icon-img {
    width: 780px;
    max-height: 700px;
    object-fit: contain;
    border-radius: 24px;
    filter: ${theme.iconFilter};
  }

  .title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 900;
    font-size: 62px;
    line-height: 1.1;
    text-align: center;
    color: ${theme.text};
    ${asset.bg === 'orange-black' ? 'text-shadow: 0 2px 12px rgba(0,0,0,0.5);' : ''}
  }

  .subtitle {
    font-size: 28px;
    color: ${theme.textSecondary};
    text-align: center;
    line-height: 1.4;
    max-width: 940px;
    ${asset.bg === 'orange-black' ? 'text-shadow: 0 1px 8px rgba(0,0,0,0.4);' : ''}
  }

  .divider {
    width: 80px;
    height: 4px;
    border-radius: 2px;
    background: ${theme.accent};
  }

  /* Metric cards row */
  .metrics-row {
    display: flex;
    gap: 20px;
    width: 100%;
    justify-content: center;
  }
  .metric-card {
    background: ${theme.cardBg};
    border: 1px solid ${theme.cardBorder};
    border-radius: 20px;
    padding: 32px 20px;
    text-align: center;
    flex: 1;
    max-width: 310px;
  }
  .metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 900;
    font-size: 44px;
    background: ${theme.metricGradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
  }
  .metric-label {
    font-size: 18px;
    color: ${theme.textSecondary};
    margin-top: 8px;
    font-weight: 600;
  }

  /* Hero metric */
  .hero-metric {
    text-align: center;
  }
  .hero-value {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 900;
    font-size: 160px;
    line-height: 1;
    background: ${theme.metricGradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .hero-label {
    font-size: 32px;
    color: ${theme.textSecondary};
    font-weight: 600;
    margin-top: 12px;
  }

  /* Comparison layout */
  .comparison {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .comp-header {
    display: flex;
    width: 100%;
  }
  .comp-header-cell {
    flex: 1;
    text-align: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 800;
    font-size: 28px;
    padding: 22px;
    border-radius: 16px;
  }
  .comp-header-left {
    background: ${asset.bg === 'white' ? 'rgba(221,51,51,0.08)' : 'rgba(255,68,68,0.12)'};
    color: ${theme.crossColor};
    margin-right: 10px;
  }
  .comp-header-right {
    background: ${asset.bg === 'white' ? 'rgba(34,170,85,0.08)' : 'rgba(68,255,136,0.12)'};
    color: ${theme.checkColor};
    margin-left: 10px;
  }
  .comp-row {
    display: flex;
    width: 100%;
    gap: 20px;
  }
  .comp-cell {
    flex: 1;
    background: ${theme.cardBg};
    border: 1px solid ${theme.cardBorder};
    border-radius: 16px;
    padding: 26px 28px;
    font-size: 24px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .comp-cell-left { color: ${theme.textSecondary}; }
  .comp-cell-right { color: ${theme.accent}; }
  .comp-icon { font-size: 22px; flex-shrink: 0; }

  /* Glass table */
  .glass-table {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .table-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: ${theme.cardBg};
    border: 1px solid ${theme.cardBorder};
    border-radius: 16px;
    padding: 26px 32px;
  }
  .table-tool {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 800;
    font-size: 28px;
    color: ${theme.text};
  }
  .table-purpose {
    font-size: 24px;
    color: ${theme.accent};
    font-weight: 600;
  }

  /* Vertical flow */
  .vertical-flow {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 0;
    position: relative;
  }
  .flow-line {
    position: absolute;
    left: 40px;
    top: 40px;
    bottom: 40px;
    width: 3px;
    background: ${theme.cardBorder};
  }
  .flow-step {
    display: flex;
    align-items: center;
    gap: 28px;
    padding: 22px 0;
    position: relative;
    z-index: 1;
  }
  .step-circle {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    background: ${theme.stepCircleBg};
    border: 3px solid ${theme.stepCircleBorder};
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 900;
    font-size: 24px;
    color: ${theme.stepCircleText};
    flex-shrink: 0;
  }
  .step-text {
    font-size: 28px;
    font-weight: 700;
    color: ${theme.text};
  }

  /* Grid */
  .grid-layout {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  .grid-item {
    background: ${theme.cardBg};
    border: 1px solid ${theme.cardBorder};
    border-radius: 20px;
    padding: 40px 28px;
    text-align: center;
  }
  .grid-value {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 800;
    font-size: 28px;
    color: ${theme.accent};
    margin-bottom: 10px;
  }
  .grid-label {
    font-size: 22px;
    font-weight: 700;
    color: ${theme.text};
  }

  /* Funnel */
  .funnel {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
  .funnel-stage {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    padding: 30px 20px;
    font-size: 24px;
    font-weight: 700;
    text-align: center;
    color: ${asset.bg === 'teal' ? '#1A1A1A' : '#ffffff'};
  }

  /* Timeline */
  .timeline {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .timeline-item {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    background: ${theme.cardBg};
    border: 1px solid ${theme.cardBorder};
    border-radius: 16px;
    padding: 22px 28px;
  }
  .timeline-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: ${theme.accent};
    margin-top: 6px;
    flex-shrink: 0;
  }
  .timeline-text {
    font-size: 22px;
    font-weight: 600;
    color: ${theme.text};
  }

  /* Branding watermark */
  .watermark {
    position: absolute;
    bottom: 40px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: ${isWhite ? 'rgba(0,0,0,0.08)' : 'rgba(255,255,255,0.06)'};
  }
</style>
</head>
<body>
<div class="story-asset">
  <div class="content-wrap">
    ${bodyContent}
  </div>
  <div class="watermark">THE COACH CONSULTANT</div>
</div>
</body>
</html>`;
}

/* ─── LAYOUT RENDERERS ─── */

function categoryTag(cat) {
  const labels = {
    'ai-systems-and-architecture': 'AI SYSTEMS',
    'flow-charts-and-processes': 'FLOW CHARTS',
    'lead-gen-and-sales-systems': 'LEAD GEN & SALES',
    'claude-ai-product-visuals': 'CLAUDE AI',
    'personal-branding-systems': 'PERSONAL BRAND'
  };
  return `<div class="tag">${labels[cat] || cat}</div>`;
}

function iconImg(asset) {
  const iconPath = `file://${path.join(ICON_BASE, asset.category, asset.icon)}`;
  return `<img class="icon-img" src="${iconPath}" alt="${asset.title}">`;
}

function metricsRow(asset) {
  if (!asset.metrics) return '';
  return `<div class="metrics-row">
    ${asset.metrics.map(m => `<div class="metric-card">
      <div class="metric-value">${m.value}</div>
      <div class="metric-label">${m.label}</div>
    </div>`).join('\n    ')}
  </div>`;
}

function layoutFullDiagram(asset) {
  return `
    ${categoryTag(asset.category)}
    <div class="title">${asset.title}</div>
    <div class="subtitle">${asset.subtitle}</div>
    <div class="divider"></div>
    ${iconImg(asset)}
    ${metricsRow(asset)}
  `;
}

function layoutMetricHero(asset) {
  return `
    ${categoryTag(asset.category)}
    <div class="title">${asset.title}</div>
    <div class="divider"></div>
    <div class="hero-metric">
      <div class="hero-value">${asset.heroValue}</div>
      <div class="hero-label">${asset.heroLabel}</div>
    </div>
    ${iconImg(asset)}
    ${metricsRow(asset)}
  `;
}

function layoutComparison(asset, theme) {
  return `
    ${categoryTag(asset.category)}
    <div class="title">${asset.title}</div>
    <div class="subtitle">${asset.subtitle}</div>
    <div class="divider"></div>
    ${iconImg(asset)}
    <div class="comparison">
      <div class="comp-header">
        <div class="comp-header-cell comp-header-left">${asset.leftLabel}</div>
        <div class="comp-header-cell comp-header-right">${asset.rightLabel}</div>
      </div>
      ${asset.rows.map(r => `<div class="comp-row">
        <div class="comp-cell comp-cell-left"><span class="comp-icon">\u2717</span> ${r.left}</div>
        <div class="comp-cell comp-cell-right"><span class="comp-icon">\u2713</span> ${r.right}</div>
      </div>`).join('\n      ')}
    </div>
  `;
}

function layoutGlassTable(asset) {
  return `
    ${categoryTag(asset.category)}
    <div class="title">${asset.title}</div>
    <div class="subtitle">${asset.subtitle}</div>
    <div class="divider"></div>
    ${iconImg(asset)}
    <div class="glass-table">
      ${asset.rows.map(r => `<div class="table-row">
        <span class="table-tool">${r.tool}</span>
        <span class="table-purpose">${r.purpose}</span>
      </div>`).join('\n      ')}
    </div>
  `;
}

function layoutVerticalFlow(asset) {
  return `
    ${categoryTag(asset.category)}
    <div class="title">${asset.title}</div>
    <div class="subtitle">${asset.subtitle}</div>
    <div class="divider"></div>
    ${iconImg(asset)}
    <div class="vertical-flow">
      <div class="flow-line"></div>
      ${asset.steps.map((s, i) => `<div class="flow-step">
        <div class="step-circle">${i + 1}</div>
        <div class="step-text">${s}</div>
      </div>`).join('\n      ')}
    </div>
  `;
}

function layoutGrid(asset) {
  return `
    ${categoryTag(asset.category)}
    <div class="title">${asset.title}</div>
    <div class="subtitle">${asset.subtitle}</div>
    <div class="divider"></div>
    ${iconImg(asset)}
    <div class="grid-layout">
      ${asset.gridItems.map(g => `<div class="grid-item">
        <div class="grid-label">${g.label}</div>
        <div class="grid-value">${g.value}</div>
      </div>`).join('\n      ')}
    </div>
  `;
}

function layoutFunnel(asset, theme) {
  const widths = [100, 85, 68, 52, 40];
  return `
    ${categoryTag(asset.category)}
    <div class="title">${asset.title}</div>
    <div class="subtitle">${asset.subtitle}</div>
    <div class="divider"></div>
    ${iconImg(asset)}
    <div class="funnel">
      ${asset.steps.map((s, i) => {
        const w = widths[i] || 40;
        const c = theme.funnelColors[i] || theme.funnelColors[0];
        return `<div class="funnel-stage" style="width: ${w}%; background: ${c};">${s}</div>`;
      }).join('\n      ')}
    </div>
  `;
}

function layoutTimeline(asset) {
  return `
    ${categoryTag(asset.category)}
    <div class="title">${asset.title}</div>
    <div class="subtitle">${asset.subtitle}</div>
    <div class="divider"></div>
    ${iconImg(asset)}
    <div class="timeline">
      ${asset.steps.map(s => `<div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-text">${s}</div>
      </div>`).join('\n      ')}
    </div>
  `;
}

/* ─── GENERATE ─── */

let count = 0;
for (const asset of manifest) {
  const theme = BG[asset.bg] || BG.dark;
  let body = '';

  switch (asset.layout) {
    case 'full-diagram':  body = layoutFullDiagram(asset); break;
    case 'metric-hero':   body = layoutMetricHero(asset); break;
    case 'comparison':    body = layoutComparison(asset, theme); break;
    case 'glass-table':   body = layoutGlassTable(asset); break;
    case 'vertical-flow': body = layoutVerticalFlow(asset); break;
    case 'grid':          body = layoutGrid(asset); break;
    case 'funnel':        body = layoutFunnel(asset, theme); break;
    case 'timeline':      body = layoutTimeline(asset); break;
    default:              body = layoutFullDiagram(asset);
  }

  const html = htmlShell(asset, theme, body);
  const outPath = path.join(assetsDir, `${asset.id}.html`);
  fs.writeFileSync(outPath, html, 'utf8');
  count++;
  console.log(`  \u2713 ${asset.id}.html (${asset.layout}, ${asset.bg})`);
}

console.log(`\nGenerated ${count} story asset HTML files in assets/`);
