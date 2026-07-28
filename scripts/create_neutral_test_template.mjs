#!/usr/bin/env node
/** Create the neutral PPTX test fixture. Requires PptxGenJS. */

import path from "node:path";
import process from "node:process";
import pptxgen from "pptxgenjs";

async function main() {
  const output = path.resolve(process.argv[2] || "neutral-template-NOT-FOR-PRODUCTION.pptx");
  const pptx = new pptxgen();
  pptx.author = "Editable Consulting PPT Workflow";
  pptx.company = "Neutral test fixture";
  pptx.subject = "Master, native object, and embedded chart workbook QA fixture";
  pptx.title = "Neutral editable presentation test template";
  pptx.lang = "en-US";
  pptx.defineLayout({ name: "NEUTRAL_WIDE", width: 13.333333, height: 7.5 });
  pptx.layout = "NEUTRAL_WIDE";
  pptx.theme = {
    headFontFace: "Arial",
    bodyFontFace: "Arial",
    lang: "en-US",
  };
  pptx.defineSlideMaster({
    title: "NEUTRAL_MASTER",
    background: { color: "FFFFFF" },
    objects: [
      {
        rect: {
          x: 0,
          y: 0,
          w: 13.333333,
          h: 0.17,
          fill: { color: "174A7E" },
          line: { color: "174A7E", transparency: 100 },
        },
      },
      {
        text: {
          text: "NEUTRAL TEST TEMPLATE · NOT FOR PRODUCTION",
          options: {
            x: 0.75,
            y: 6.78,
            w: 8.6,
            h: 0.22,
            fontFace: "Arial",
            fontSize: 8,
            color: "6D7882",
            margin: 0,
          },
        },
      },
      {
        rect: {
          x: 11.88,
          y: 0.52,
          w: 0.72,
          h: 0.3,
          fill: { color: "174A7E" },
          line: { color: "174A7E" },
        },
      },
      {
        text: {
          text: "LOGO",
          options: {
            x: 11.96,
            y: 0.585,
            w: 0.56,
            h: 0.14,
            fontFace: "Arial",
            fontSize: 8,
            bold: true,
            color: "FFFFFF",
            align: "center",
            margin: 0,
          },
        },
      },
    ],
    slideNumber: {
      x: 12.2,
      y: 6.78,
      w: 0.4,
      h: 0.22,
      fontFace: "Arial",
      fontSize: 8,
      color: "6D7882",
      align: "right",
      margin: 0,
    },
  });

  const slide1 = pptx.addSlide("NEUTRAL_MASTER");
  slide1.addText("Editable workflow test fixture", {
    x: 0.75,
    y: 0.78,
    w: 10.6,
    h: 0.58,
    fontFace: "Arial",
    fontSize: 24,
    bold: true,
    color: "17324D",
    margin: 0,
  });
  slide1.addShape(pptx.ShapeType.rect, {
    x: 0.75,
    y: 1.7,
    w: 11.85,
    h: 4.35,
    fill: { color: "F7F9FB" },
    line: { color: "D5DDE5", width: 1 },
  });
  slide1.addText("此文件仅用于结构与质量检查，不得替代用户提供的母版。", {
    x: 1.15,
    y: 2.3,
    w: 10.2,
    h: 0.45,
    fontFace: "Microsoft YaHei",
    fontSize: 19,
    bold: true,
    color: "17324D",
    margin: 0,
  });
  slide1.addText(
    "This file demonstrates a native slide master, editable text and shapes, and inherited page numbering.",
    {
      x: 1.15,
      y: 3.15,
      w: 9.5,
      h: 0.6,
      fontFace: "Arial",
      fontSize: 16,
      color: "526273",
      margin: 0,
    },
  );

  const slide2 = pptx.addSlide("NEUTRAL_MASTER");
  slide2.addText("Native chart with editable embedded data", {
    x: 0.75,
    y: 0.78,
    w: 10.6,
    h: 0.58,
    fontFace: "Arial",
    fontSize: 24,
    bold: true,
    color: "17324D",
    margin: 0,
  });
  slide2.addShape(pptx.ShapeType.rect, {
    x: 0.75,
    y: 1.7,
    w: 11.85,
    h: 4.35,
    fill: { color: "F7F9FB" },
    line: { color: "D5DDE5", width: 1 },
  });
  slide2.addChart(
    pptx.ChartType.bar,
    [{ name: "Completion", labels: ["Clarify", "Approve SVG", "Build", "Verify"], values: [100, 100, 100, 100] }],
    {
      x: 1.2,
      y: 2.3,
      w: 7.2,
      h: 2.9,
      catAxisLabelFontFace: "Arial",
      catAxisLabelFontSize: 11,
      valAxisLabelFontFace: "Arial",
      valAxisLabelFontSize: 10,
      showLegend: false,
      showValue: true,
      showTitle: false,
      showCatName: false,
      chartColors: ["174A7E"],
      dataLabelPosition: "outEnd",
      valAxisMinVal: 0,
      valAxisMaxVal: 120,
    },
  );
  slide2.addText(
    "Quantitative charts must remain native and keep an editable Excel workbook inside the PPTX.",
    {
      x: 9.15,
      y: 2.65,
      w: 2.55,
      h: 1.5,
      fontFace: "Arial",
      fontSize: 16,
      bold: true,
      color: "17324D",
      margin: 0,
      breakLine: false,
    },
  );

  await pptx.writeFile({ fileName: output });
  process.stdout.write(`${output}\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
