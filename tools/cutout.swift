// Hapus latar foto memakai Vision (macOS 14+), tanpa unduhan model.
// Pakai: swiftc -O tools/cutout.swift -o /tmp/cutout && /tmp/cutout masuk.png keluar-mask.png
// Hasil: PNG grayscale berisi mask subjek (putih = subjek).
import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
guard args.count == 3 else { print("pakai: cutout <masuk> <keluar-mask.png>"); exit(2) }
guard let img = NSImage(contentsOfFile: args[1]), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("gagal membuka gambar"); exit(1) }

let handler = VNImageRequestHandler(cgImage: cg, options: [:])
let req = VNGenerateForegroundInstanceMaskRequest()
req.usesCPUOnly = true
try handler.perform([req])
guard let obs = req.results?.first else { print("tidak ada subjek"); exit(1) }
print("jumlah subjek:", obs.allInstances.count)
let buf = try obs.generateScaledMaskForImage(forInstances: obs.allInstances, from: handler)
let ci = CIImage(cvPixelBuffer: buf)
let ctx = CIContext()
guard let out = ctx.createCGImage(ci, from: ci.extent) else { print("gagal membuat mask"); exit(1) }
let rep = NSBitmapImageRep(cgImage: out)
try rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[2]))
print("mask tersimpan", out.width, "x", out.height)
