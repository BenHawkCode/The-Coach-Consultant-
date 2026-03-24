/**
 * ============================================================
 * CLAUDE PROJECTS CLIENT PACK — MASTER INDEX GENERATOR
 * ============================================================
 *
 * This Google Apps Script scans your Client Pack folder in
 * Google Drive and automatically builds a fully hyperlinked
 * Google Sheet index so clients can click through to any
 * document instantly.
 *
 * HOW TO USE:
 *
 * 1. Go to https://script.google.com
 * 2. Click "New Project"
 * 3. Delete any code already in the editor
 * 4. Paste this ENTIRE script into the editor
 * 5. Click the save icon (or Ctrl+S / Cmd+S)
 * 6. Name the project "Client Pack Index Generator"
 * 7. In the function dropdown at the top, select "createMasterIndex"
 * 8. Click the Run button (▶)
 * 9. When prompted, click "Review permissions" → choose your
 *    Google account → click "Allow"
 * 10. Wait 30-60 seconds. A new Google Sheet called
 *     "📋 MASTER INDEX — Start Here" will appear in your
 *     Client Pack folder.
 *
 * IMPORTANT: Update the FOLDER_ID below with your actual
 * Google Drive folder ID before running.
 *
 * Your folder ID is the string after /folders/ in your URL:
 * https://drive.google.com/drive/folders/YOUR_FOLDER_ID
 * ============================================================
 */

// ─── CONFIGURATION ───
// Replace this with YOUR Google Drive folder ID
var FOLDER_ID = "14hjViNcXX8LgIN_ke2kZwthIBe_eCmUf";

// ─── FILE DESCRIPTIONS ───
// Lookup table for every file in the pack

var DESCRIPTIONS = {
  // 00-Onboarding
  "00-COST-SAVINGS-BREAKDOWN.docx": "What this system replaces: £62,450/month in staff wages broken down by role",
  "01-YOUR-FIRST-15-MINUTES.docx": "Set up your first project in 15 minutes with zero knowledge files needed",
  "02-START-HERE.docx": "Full orientation guide with screenshots showing how to set up any Claude Project",
  "03-DEFINE-YOUR-BRAND-FIRST.docx": "Fill-in worksheet for the 7 placeholders used in every project template",
  "04-WHY-YOU-NEED-PRO-AND-MAX.docx": "Which Claude plan to choose and why the free plan will not work",
  "05-RECOMMENDED-TOOLS-AND-SETUP.docx": "Wispr Flow, browser setup, and how to prepare your knowledge files",
  "06-KNOWLEDGE-FILE-STARTER-KIT.docx": "How to find, create, and organise the files your projects need",
  "07-YOUR-FIRST-WEEK-FRAMEWORK.docx": "Day-by-day setup plan plus Month 1 and Quarter 1 rollout sequence",
  "08-HOW-TO-GET-BEST-RESULTS.docx": "5 rules for writing prompts that get you what you want first time",
  "09-ALL-34-PROJECTS-AT-A-GLANCE.docx": "Every project with ROI ratings, difficulty levels, and Top 5 recommendations",
  "10-SETUP-PROGRESS-TRACKER.docx": "Tick-off checklist to track your setup across 5 phases",
  "11-TROUBLESHOOTING-AND-FAQS.docx": "Quick fixes for the most common issues",
  "12-PROJECT-REVIEW-CHECKLIST.docx": "Per-project setup checklist for all 34 projects",

  // 01-Content-Marketing
  "01-Content-Strategy-Calendar.docx": "Project 1: Plan monthly themes and weekly content calendars",
  "02-Blog-Long-Form-Content.docx": "Project 2: SEO articles, guides, and thought leadership pieces",
  "03-Email-Marketing-Sequences.docx": "Project 3: Welcome sequences, nurture campaigns, launch emails",
  "04-Lead-Magnets-Opt-In.docx": "Project 4: Checklists, guides, and downloadable resources",
  "33-Community-Management.docx": "Project 33: Group rules, welcome sequences, engagement content",

  // 02-Social-Media
  "05-Instagram-Content-Creator.docx": "Project 5: Captions, carousels, reel scripts, stories",
  "06-LinkedIn-Thought-Leadership.docx": "Project 6: Posts, articles, connection messages",
  "07-YouTube-Content-Scripts.docx": "Project 7: Full scripts with timestamps, titles, descriptions",
  "08-Content-Repurposing-Engine.docx": "Project 8: Turn one piece of content into five platforms",
  "32-Podcast-Strategy-Guest-Appearances.docx": "Project 32: Topic lists, speaker bios, podcast pitches",

  // 03-Sales-Lead-Generation
  "09-Sales-Landing-Page-Copy.docx": "Project 9: High-converting sales pages and landing pages",
  "10-Proposal-Pitch-Writer.docx": "Project 10: Client proposals, pitch decks, follow-ups",
  "11-DM-Outreach-Sequences.docx": "Project 11: Personalised outreach and follow-up scripts",
  "12-Webinar-Workshop-Planner.docx": "Project 12: Webinar structure, scripts, follow-up sequences",

  // 04-Client-Fulfilment
  "13-Client-Onboarding-Assistant.docx": "Project 13: Welcome packets, onboarding emails, intake forms",
  "14-Coaching-Session-Prep-Notes.docx": "Project 14: Session agendas, questions, follow-up summaries",
  "15-Client-Reporting-Results.docx": "Project 15: Monthly reports, progress summaries, ROI breakdowns",
  "16-Course-Programme-Content.docx": "Project 16: Module outlines, lesson scripts, workbook pages",
  "31-Client-Offboarding-Retention.docx": "Project 31: Offboarding sequences, referral systems, alumni offers",

  // 05-Operations
  "17-SOP-Process-Documentation.docx": "Project 17: Step-by-step procedures and training guides",
  "18-KPI-Business-Reporting.docx": "Project 18: Metrics analysis, performance reports, trend spotting",
  "19-Team-Communication-Management.docx": "Project 19: Team updates, meeting agendas, feedback reviews",
  "20-Finance-Invoicing-Assistant.docx": "Project 20: Pricing structures, invoice templates, budgets",
  "29-Finance-Strategic-Reporting.docx": "Project 29: Revenue breakdowns, forecasting, CFO-level analysis",
  "34-Tech-Stack-Automation-Setup.docx": "Project 34: Tool recommendations, automation workflows",

  // 06-Strategy-Growth
  "21-Business-Strategy-Planning.docx": "Project 21: Quarterly plans, goal setting, business vision",
  "22-Brand-Positioning-Strategist.docx": "Project 22: Brand identity, positioning, differentiation",
  "23-Partnership-Collaboration.docx": "Project 23: JV partners, cross-promotion, collaboration planning",
  "24-Customer-Research-Insights.docx": "Project 24: Market research, customer insights, competitive analysis",
  "30-Offer-Design-Pricing-Strategy.docx": "Project 30: Offer architecture, pricing, offer waterfall",

  // 07-Admin-Organisation
  "25-Email-Communication-Manager.docx": "Project 25: Email templates, FAQs, communication standards",
  "26-Meeting-Event-Coordinator.docx": "Project 26: Agendas, event checklists, follow-up templates",
  "27-Legal-Compliance-Drafts.docx": "Project 27: Terms, privacy policies, disclaimers, contracts",
  "28-Personal-Productivity-Planning.docx": "Project 28: Weekly planning, priorities, goal setting",

  // 08-Claude-Code-Guides
  "00-WHAT-IS-CLAUDE-CODE.docx": "What Claude Code is, when to use it, and how to use the prompts in this folder",
  "01-FULL-REBRAND-UPDATE.docx": "Update brand files, names, and messaging across all projects at once",
  "02-BULK-CTA-UPDATE.docx": "Change your website URL, booking link, or CTA across every project",
  "03-PRICING-AND-OFFER-UPDATE.docx": "Update pricing, launch new offers, retire old ones across all projects",
  "04-TARGET-AUDIENCE-UPDATE.docx": "Push audience or niche changes to every project",
  "05-QUARTERLY-HEALTH-CHECK.docx": "Full audit of all projects for accuracy, consistency, and optimisation",
  "06-NEW-KNOWLEDGE-FILE-ROLLOUT.docx": "Add a new document to the right projects without missing any",
  "07-VOICE-AND-TONE-RECALIBRATION.docx": "Recalibrate your voice across all writing projects",
  "08-SEASONAL-CAMPAIGN-SETUP.docx": "Temporarily update projects for a launch or promo with revert guide",
  "09-PROJECT-BACKUP-AND-EXPORT.docx": "Create a full snapshot of all project configurations",
  "10-NEW-PROJECT-SETUP-GUIDED.docx": "Claude Code walks you through setting up a new project step by step",
  "11-COMPLIANCE-AND-DISCLAIMER-UPDATE.docx": "Audit and update legal disclaimers across all projects",
  "12-TEAM-VA-HANDOVER-PACK.docx": "Generate a complete handover document for a team member or VA",

  // Navigation files
  "00-MASTER-INDEX.docx": "Master navigation document — map of every file in the pack",
  "00-FOLDER-INDEX.docx": "Folder contents and navigation guide",
};

// ─── FOLDER DISPLAY ORDER ───

var FOLDER_ORDER = [
  "00-Onboarding",
  "01-Content-Marketing",
  "02-Social-Media",
  "03-Sales-Lead-Generation",
  "04-Client-Fulfilment",
  "05-Operations",
  "06-Strategy-Growth",
  "07-Admin-Organisation",
  "08-Claude-Code-Guides"
];

var FOLDER_TITLES = {
  "00-Onboarding": "📂 00 — Onboarding (Start Here)",
  "01-Content-Marketing": "📂 01 — Content Marketing",
  "02-Social-Media": "📂 02 — Social Media",
  "03-Sales-Lead-Generation": "📂 03 — Sales & Lead Generation",
  "04-Client-Fulfilment": "📂 04 — Client Fulfilment & Delivery",
  "05-Operations": "📂 05 — Operations & Business Management",
  "06-Strategy-Growth": "📂 06 — Strategy & Growth",
  "07-Admin-Organisation": "📂 07 — Admin & Organisation",
  "08-Claude-Code-Guides": "📂 08 — Claude Code Guides"
};


// ─── MAIN FUNCTION ───

function createMasterIndex() {
  var rootFolder = DriveApp.getFolderById(FOLDER_ID);

  // Collect all files grouped by folder
  var folderData = {};

  // Get files in root
  var rootFiles = rootFolder.getFiles();
  while (rootFiles.hasNext()) {
    var file = rootFiles.next();
    if (!folderData["_root"]) folderData["_root"] = [];
    folderData["_root"].push({
      name: file.getName(),
      url: file.getUrl()
    });
  }

  // Get subfolders and their files
  var subfolders = rootFolder.getFolders();
  while (subfolders.hasNext()) {
    var subfolder = subfolders.next();
    var folderName = subfolder.getName();
    folderData[folderName] = [];

    var files = subfolder.getFiles();
    while (files.hasNext()) {
      var file = files.next();
      folderData[folderName].push({
        name: file.getName(),
        url: file.getUrl()
      });
    }

    // Sort files by name within each folder
    folderData[folderName].sort(function(a, b) {
      return a.name.localeCompare(b.name);
    });
  }

  // Create or find the spreadsheet
  var sheetName = "📋 MASTER INDEX — Start Here";
  var spreadsheet;

  // Check if sheet already exists in the folder
  var existingFiles = rootFolder.getFilesByName(sheetName);
  if (existingFiles.hasNext()) {
    var existingFile = existingFiles.next();
    spreadsheet = SpreadsheetApp.openById(existingFile.getId());
  } else {
    spreadsheet = SpreadsheetApp.create(sheetName);
    // Move to the pack folder
    var ssFile = DriveApp.getFileById(spreadsheet.getId());
    rootFolder.addFile(ssFile);
    DriveApp.getRootFolder().removeFile(ssFile);
  }

  var sheet = spreadsheet.getActiveSheet();
  sheet.clear();
  sheet.setName("Master Index");

  // ─── Build the sheet ───
  var row = 1;

  // Title
  sheet.getRange(row, 1).setValue("Claude Projects Client Pack — Master Index");
  sheet.getRange(row, 1, 1, 4).merge();
  sheet.getRange(row, 1).setFontFamily("Poppins")
    .setFontSize(18)
    .setFontWeight("bold")
    .setFontColor("#1a1a2e");
  row += 1;

  // Subtitle
  sheet.getRange(row, 1).setValue("Click any document name to open it directly. Start with the Onboarding folder (documents 00-12 in order).");
  sheet.getRange(row, 1, 1, 4).merge();
  sheet.getRange(row, 1).setFontFamily("Poppins")
    .setFontSize(10)
    .setFontColor("#555555");
  row += 1;

  // Reading order
  sheet.getRange(row, 1).setValue("📖 Reading order: 00 Cost Savings → 01 First 15 Min → 02 Start Here → 03 Brand Clarity → 04 Pro/Max → 05 Tools → 06 Knowledge Files → 07 First Week → 08 Prompting → 09 Overview → 10 Tracker → 11 FAQ → 12 Checklist");
  sheet.getRange(row, 1, 1, 4).merge();
  sheet.getRange(row, 1).setFontFamily("Poppins")
    .setFontSize(9)
    .setFontColor("#006633")
    .setFontWeight("bold");
  row += 2;

  // Header row
  var headers = ["Folder", "Document", "Description", "Direct Link"];
  sheet.getRange(row, 1, 1, 4).setValues([headers]);
  sheet.getRange(row, 1, 1, 4)
    .setFontFamily("Poppins")
    .setFontSize(10)
    .setFontWeight("bold")
    .setFontColor("#ffffff")
    .setBackground("#1a1a2e")
    .setHorizontalAlignment("left");
  sheet.setFrozenRows(row);
  row += 1;

  var dataStartRow = row;
  var isAlternate = false;

  // Process each folder in order
  for (var i = 0; i < FOLDER_ORDER.length; i++) {
    var folderKey = FOLDER_ORDER[i];
    var files = folderData[folderKey] || [];
    var folderTitle = FOLDER_TITLES[folderKey] || folderKey;

    // Folder header row
    sheet.getRange(row, 1).setValue(folderTitle);
    sheet.getRange(row, 1, 1, 4).merge();
    sheet.getRange(row, 1)
      .setFontFamily("Poppins")
      .setFontSize(11)
      .setFontWeight("bold")
      .setFontColor("#1a5ab8")
      .setBackground("#f0f4ff");
    row += 1;

    // File rows
    for (var j = 0; j < files.length; j++) {
      var file = files[j];
      var desc = DESCRIPTIONS[file.name] || "";
      var bgColor = isAlternate ? "#f9f9f9" : "#ffffff";

      // Create hyperlink formula for the document name
      var linkFormula = '=HYPERLINK("' + file.url + '", "' + file.name.replace(/"/g, '""') + '")';

      sheet.getRange(row, 1).setValue(folderKey);
      sheet.getRange(row, 2).setFormula(linkFormula);
      sheet.getRange(row, 3).setValue(desc);
      sheet.getRange(row, 4).setValue(file.url);

      // Style the row
      sheet.getRange(row, 1, 1, 4).setBackground(bgColor);
      sheet.getRange(row, 1).setFontFamily("Poppins").setFontSize(9).setFontColor("#888888");
      sheet.getRange(row, 2).setFontFamily("Poppins").setFontSize(10).setFontColor("#1a5ab8").setFontWeight("bold");
      sheet.getRange(row, 3).setFontFamily("Poppins").setFontSize(9).setFontColor("#555555");
      sheet.getRange(row, 4).setFontFamily("Poppins").setFontSize(8).setFontColor("#aaaaaa");

      isAlternate = !isAlternate;
      row += 1;
    }

    // Spacer row between folders
    row += 1;
    isAlternate = false;
  }

  // Root-level files (Master Index etc.)
  if (folderData["_root"] && folderData["_root"].length > 0) {
    sheet.getRange(row, 1).setValue("📂 Root Folder");
    sheet.getRange(row, 1, 1, 4).merge();
    sheet.getRange(row, 1)
      .setFontFamily("Poppins")
      .setFontSize(11)
      .setFontWeight("bold")
      .setFontColor("#1a5ab8")
      .setBackground("#f0f4ff");
    row += 1;

    var rootFilesSorted = folderData["_root"].sort(function(a, b) {
      return a.name.localeCompare(b.name);
    });

    for (var k = 0; k < rootFilesSorted.length; k++) {
      var rFile = rootFilesSorted[k];
      var rDesc = DESCRIPTIONS[rFile.name] || "";
      var linkFormula = '=HYPERLINK("' + rFile.url + '", "' + rFile.name.replace(/"/g, '""') + '")';

      sheet.getRange(row, 1).setValue("Root");
      sheet.getRange(row, 2).setFormula(linkFormula);
      sheet.getRange(row, 3).setValue(rDesc);
      sheet.getRange(row, 4).setValue(rFile.url);

      sheet.getRange(row, 1).setFontFamily("Poppins").setFontSize(9).setFontColor("#888888");
      sheet.getRange(row, 2).setFontFamily("Poppins").setFontSize(10).setFontColor("#1a5ab8").setFontWeight("bold");
      sheet.getRange(row, 3).setFontFamily("Poppins").setFontSize(9).setFontColor("#555555");
      sheet.getRange(row, 4).setFontFamily("Poppins").setFontSize(8).setFontColor("#aaaaaa");

      row += 1;
    }
  }

  // ─── Final formatting ───

  // Column widths
  sheet.setColumnWidth(1, 180);  // Folder
  sheet.setColumnWidth(2, 320);  // Document
  sheet.setColumnWidth(3, 450);  // Description
  sheet.setColumnWidth(4, 350);  // Link

  // Summary at the bottom
  row += 1;
  var totalFiles = 0;
  for (var key in folderData) {
    totalFiles += folderData[key].length;
  }

  sheet.getRange(row, 1).setValue("Total documents: " + totalFiles);
  sheet.getRange(row, 1, 1, 4).merge();
  sheet.getRange(row, 1)
    .setFontFamily("Poppins")
    .setFontSize(10)
    .setFontWeight("bold")
    .setFontColor("#006633");

  Logger.log("✅ Master Index created successfully with " + totalFiles + " documents.");
  Logger.log("📋 Sheet: " + spreadsheet.getUrl());
}
