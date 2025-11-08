use std::io::{self, Write};
use std::ptr;
use std::sync::atomic::{compiler_fence, Ordering};
use std::time::Duration;

/// XOR key (flag stored XOR-encoded in the binary)
const XOR_KEY: u8 = 0x42;

/// Encoded bytes (XOR with XOR_KEY yields the plaintext flag).
/// Stored as a byte literal so there is no plain "CHC{...}" string in the binary.
const ENCODED_BYTES: &[u8] = b"\x01\n\x0192v5&q\x1d+,$+.60v6q&\x1d 0q#)\x1d6*q\x1d$.-5?";

/// Small briefing printed at startup (funny, not hint-y).
fn briefing() {
    println!("--- BRIEF: Pawde's Snack Recon ---");
    println!("Pawde swears it was 'an experiment' with the office toaster.");
    println!("We can't prove anything yet. Your job is simple: confirm the payload.");
    println!("----------------------------------");
}

/// Decode ENCODED_BYTES into `dst` using volatile writes (keeps bytes in memory).
/// Returns the number of bytes written.
fn write_decoded_to_buffer(dst: &mut [u8]) -> usize {
    let n = ENCODED_BYTES.len().min(dst.len());
    for i in 0..n {
        let dec = ENCODED_BYTES[i] ^ XOR_KEY;
        // volatile write so compiler is less likely to optimize this away
        unsafe { ptr::write_volatile(&mut dst[i], dec) };
    }
    compiler_fence(Ordering::SeqCst);
    n
}

/// Read decoded bytes from buffer with volatile reads into a Vec<u8>.
fn read_decoded_from_buffer(buf: &[u8], n: usize) -> Vec<u8> {
    let mut out = Vec::with_capacity(n);
    for i in 0..n {
        let b = unsafe { ptr::read_volatile(&buf[i]) };
        out.push(b);
    }
    out
}

/// Wipe buffer with junk using volatile writes.
fn wipe_buffer(buf: &mut [u8]) {
    for i in 0..buf.len() {
        unsafe { ptr::write_volatile(&mut buf[i], b'x') };
    }
    compiler_fence(Ordering::SeqCst);
}

/// Print success and the flag (reads the flag from the volatile buffer).
fn printing(buf: &[u8], n: usize) {
    let v = read_decoded_from_buffer(buf, n);
    if let Ok(_s) = String::from_utf8(v) {
        println!("Access granted. Congrats — you did it. \nPawde has been put to jail now");
    } else {
        println!("Access granted. (flag decoding error)");
    }
}

/// The gateway: decode the flag into a stack buffer, ask user to type the flag,
/// compare input to the decoded flag, and either reveal or wipe.
fn gateway() {
    // stack-local buffer to hold the decoded flag bytes
    let mut flag_buf = [0u8; 64];

    // decode into buffer (happens at runtime, right before the check)
    let n = write_decoded_to_buffer(&mut flag_buf);

    // small fence to discourage reordering
    compiler_fence(Ordering::SeqCst);

    // Prompt the user to type the flag exactly.
    print!("Enter the flag: ");
    io::stdout().flush().ok();

    let mut attempt = String::new();
    if io::stdin().read_line(&mut attempt).is_err() {
        wipe_buffer(&mut flag_buf);
        println!("Input error.");
        return;
    }

    // Trim trailing newline/carriage returns only.
    let attempt = attempt.trim_end_matches(&['\r', '\n'][..]);

    // Read decoded flag from buffer into a String for a straightforward, exact comparison.
    let decoded = read_decoded_from_buffer(&flag_buf, n);
    match String::from_utf8(decoded) {
        Ok(flag_string) => {
            if attempt == flag_string {
                // Success: print the flag from memory.
                printing(&flag_buf, n);
            } else {
                // Wrong input: immediately overwrite the in-memory flag.
                wipe_buffer(&mut flag_buf);
                println!("Access denied.");
            }
        }
        Err(_) => {
            // decoding problem: wipe and exit.
            wipe_buffer(&mut flag_buf);
            println!("Access denied.");
        }
    }

    // keep process alive briefly so an analyst can attach if needed
    std::thread::sleep(Duration::from_secs(2));
}

fn main() {
    briefing();
    println!("Starting verification...");
    gateway();
    println!("Session ended.");
}
