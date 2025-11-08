# Solve.md

1. Go to:

   ```
   %LocalAppData%\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState
   ```

   and find  **plum.sqlite** .
2. Open `plum.sqlite` in **DB Browser for SQLite** (or any SQLite viewer).
3. Browse the **Note** table → check the **Text** column.
4. One of the notes contains a  **Base32-encoded string** .
5. Copy that string and decode it using:

   ```bash
   echo "BASE32_STRING" | base32 --decode
   ```

   or an online Base32 decoder.
6. The decoded text gives the flag:

   ```
   c0ngr4ts_y0u_f0und_my_n0t3s
   ```

---

That’s the entire solve — find the encoded note in `plum.sqlite`, decode it, get the flag.
