# Format an SD Card After Raspberry Pi OS: A to Z (Windows)
*Restore a Raspberry Pi / Linux boot SD card so Windows can use it again*

A card that has run Raspberry Pi OS (or any Linux) is split into a small boot partition and a Linux data partition. Windows only understands part of that layout, so the card shows up tiny, refuses new files, and the normal **Format** option fails. The card is not broken. The fix is to wipe the partition layout with `diskpart` and rebuild one Windows-friendly partition.

> **Warning:** **This erases everything on the card, permanently.** Also, `clean` wipes whichever disk is selected. If you select your PC's hard drive by mistake, it is gone for good. Verify the disk number twice.

## 1. What you need

- A Windows PC with an SD slot, or a USB SD card reader
- Administrator rights on the PC
- A backup of anything you want to keep from the card (copy it off first)
- About 5 to 10 minutes

## 2. Step-by-step procedure

### Step 1: Insert the card

Plug the SD card into the PC. If Windows pops up a message saying you need to format the disk, click **Cancel**. Do not format from that prompt. You may see only a small drive (often called `bootfs`) or nothing at all. That is normal for a Pi card.

### Step 2: Open Command Prompt as Administrator

Press the Windows key, type `cmd`, then choose **Run as administrator**. A black command window opens.

### Step 3: Start diskpart

```
diskpart
```

Press Enter. The prompt changes to `DISKPART>`, which confirms you are in the right tool.

### Step 4: List all disks and find the SD card

```
list disk
```

Match the card by its size (for example, a 16 GB card shows as roughly 14 to 15 GB). Not sure which one it is? Remove the card, run `list disk`, note the entries, reinsert the card and run it again. The new entry is your card.

### Step 5: Select the SD card

```
select disk 3
```

Replace `3` with your card's disk number. Diskpart replies that the disk is now selected.

### Step 6: Double-check the selection

```
list disk
```

The selected disk now has an asterisk (`*`) beside it. Make sure it is the SD card. Optional extra check: `detail disk` shows the model and size of the selected disk.

### Step 7: Clean the card (point of no return)

```
clean
```

This removes the boot and Linux partitions, which are what block Windows. Expect the message "DiskPart succeeded in cleaning the disk." If it errors, run `clean` once more.

### Step 8: Create one partition that fills the card

```
create partition primary
```

The card is now blank with nowhere to store files, so this creates a single primary partition using the whole capacity.

### Step 9: Format the partition

```
format fs=fat32 quick
```

FAT32 works on Windows, Mac and Linux. The progress may sit at 0% for several seconds and then jump to 100%, which is normal. Finish message: "DiskPart successfully formatted the volume." Cards larger than 32 GB: see the file system section below and use `format fs=exfat quick` instead.

### Step 10: Give it a drive letter (only if needed)

```
assign
```

Windows usually mounts the card by itself after formatting. If no drive letter appears, run `assign` (or `assign letter=F` to choose one).

### Step 11: Exit and check the result

```
exit
```

Close the Command Prompt, open File Explorer and confirm the card shows its full capacity. Copy a small test file onto it and open it to confirm it works.

## 3. Command cheat sheet

| Command | What it does |
|---|---|
| `diskpart` | Starts the disk partition tool |
| `list disk` | Shows all connected disks (selected one is marked *) |
| `select disk N` | Selects the disk numbered N |
| `detail disk` | Shows model and size of the selected disk (optional check) |
| `clean` | Erases the partition table and all partitions |
| `create partition primary` | Makes one partition using all space |
| `format fs=fat32 quick` | Quick-formats the partition as FAT32 |
| `assign` | Assigns a drive letter if none was given |
| `exit` | Leaves diskpart |

## 4. Which file system should you pick?

| File system | Command | Best for |
|---|---|---|
| FAT32 | `format fs=fat32 quick` | Maximum compatibility (Windows, Mac, Linux, cameras, many devices). Max 4 GB per file. Windows will not format volumes above 32 GB as FAT32. |
| exFAT | `format fs=exfat quick` | Larger cards (64 GB and up) and big files. Works on modern Windows, Mac and Linux; some older devices cannot read it. |
| NTFS | `format fs=ntfs quick` | Windows-only use. Poor choice for cameras or other devices. |

## 5. Troubleshooting

- **Card was tiny before I started:** that is the symptom being fixed. After Step 9 it returns to full size.
- **`clean` shows an error:** confirm the prompt is running as administrator, then run `clean` again.
- **Card is read-only or write-protected:** slide the lock switch on the SD adapter to the unlocked position, or run `attributes disk clear readonly` while the disk is selected, then repeat from Step 7.
- **Diskpart still cannot clean or read the card:** write any OS image over it first using Raspberry Pi Imager (the image does not matter, it just overwrites the layout), then repeat this procedure from Step 2.
- **Card not listed by `list disk`:** try a different USB port or card reader, and check the card is fully seated.
- **Still failing after all of this:** the card may be worn out or faulty and is worth replacing.

## 6. Optional: put Raspberry Pi OS back on the card

Use Raspberry Pi Imager: choose your Pi model, choose the OS, choose the SD card as storage, then write. After that, the card will look odd to Windows again. Repeat this guide whenever you want to reclaim it.

## 7. Safety checklist

- Backup done before starting
- Command Prompt opened as administrator
- Card disk number confirmed twice with `list disk` (asterisk on the right disk)
- Only then run `clean`

---
*Based on the Bytes N Bits video "Fix Your SD Card After Using It As a Raspberry Pi or Linux Boot Disk" (youtu.be/DdCmPeE8kRU) and its project page at bytesnbits.co.uk/reformat-raspberry-pi-boot-sd-card. Steps 1 to 9 and 11 follow that guide. The `detail disk`, `assign`, file system notes and troubleshooting were added for completeness.*
