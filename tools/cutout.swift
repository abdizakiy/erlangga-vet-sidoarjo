// Pisahkan subjek dari latar memakai Vision (macOS 14+), tanpa unduhan model.
// Pakai: swiftc -O tools/cutout.swift -o /tmp/cutout
//        /tmp/cutout masuk.png mask-gabungan.png [peta-objek.png]
// mask-gabungan.png: putih = semua subjek. peta-objek.png (opsional): tiap piksel
// bernilai nomor objek (0 = latar), supaya objek bisa dipilih satu per satu.
import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else { print("pakai: cutout <masuk> <mask.png> [peta-objek.png]"); exit(2) }
guard let img = NSImage(contentsOfFile: args[1]), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("gagal membuka gambar"); exit(1) }

let handler = VNImageRequestHandler(cgImage: cg, options: [:])
let req = VNGenerateForegroundInstanceMaskRequest()
req.usesCPUOnly = true
try handler.perform([req])
guard let obs = req.results?.first else { print("tidak ada subjek"); exit(1) }
print("jumlah objek:", obs.allInstances.count, obs.allInstances.sorted())

func savePNG(_ ci: CIImage, _ path: String) throws {
    let ctx = CIContext()
    guard let out = ctx.createCGImage(ci, from: ci.extent) else { print("gagal membuat gambar"); exit(1) }
    let rep = NSBitmapImageRep(cgImage: out)
    try rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: path))
}
let buf = try obs.generateScaledMaskForImage(forInstances: obs.allInstances, from: handler)
try savePNG(CIImage(cvPixelBuffer: buf), args[2])

if args.count >= 4 {
    // peta objek: 1 byte per piksel
    let m = obs.instanceMask
    CVPixelBufferLockBaseAddress(m, .readOnly)
    let w = CVPixelBufferGetWidth(m), h = CVPixelBufferGetHeight(m), bpr = CVPixelBufferGetBytesPerRow(m)
    let base = CVPixelBufferGetBaseAddress(m)!.assumingMemoryBound(to: UInt8.self)
    var data = [UInt8](repeating: 0, count: w * h)
    for y in 0..<h { for x in 0..<w { data[y * w + x] = base[y * bpr + x] } }
    CVPixelBufferUnlockBaseAddress(m, .readOnly)
    let cs = CGColorSpaceCreateDeviceGray()
    let provider = CGDataProvider(data: Data(data) as CFData)!
    let gimg = CGImage(width: w, height: h, bitsPerComponent: 8, bitsPerPixel: 8, bytesPerRow: w, space: cs, bitmapInfo: CGBitmapInfo(rawValue: 0), provider: provider, decode: nil, shouldInterpolate: false, intent: .defaultIntent)!
    let rep = NSBitmapImageRep(cgImage: gimg)
    try rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[3]))
    print("peta objek", w, "x", h)
}
