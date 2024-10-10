import math
import sys

A = 0
B = 0

# Pre-create the Z-buffer and frame buffer, avoiding allocation in each frame
z_buffer = [0] * 1760
frame_buffer = [' '] * 1760

# Pre-create a string to represent the entire ASCII character set we use
ascii_chars = '.,-~:;=!*#$@'

# Clear the screen once at the start and move cursor back at each frame
sys.stdout.write('\x1b[2J')

while True:
    # Reset buffers for the new frame
    z_buffer[:] = [0] * 1760
    frame_buffer[:] = [' '] * 1760
    
    # Precompute sine and cosine for A and B once per frame
    sin_A = math.sin(A)
    cos_A = math.cos(A)
    sin_B = math.sin(B)
    cos_B = math.cos(B)

    for j in range(0, 628, 7):  # Theta (rotation around vertical axis)
        cos_j = math.cos(j)
        sin_j = math.sin(j)

        for i in range(0, 628, 2):  # Phi (rotation around horizontal axis)
            sin_i = math.sin(i)
            cos_i = math.cos(i)

            h = cos_j + 2
            D = 1 / (sin_i * h * sin_A + sin_j * cos_A + 5)
            t = sin_i * h * cos_A - sin_j * sin_A

            # Calculate screen coordinates (x, y)
            x = int(40 + 30 * D * (cos_i * h * cos_B - t * sin_B))
            y = int(12 + 15 * D * (cos_i * h * sin_B + t * cos_B))
            o = x + 80 * y

            # Determine brightness index (N)
            N = int(8 * ((sin_j * sin_A - sin_i * cos_j * cos_A) * cos_B 
                        - sin_i * cos_j * sin_A - sin_j * cos_A 
                        - cos_i * cos_j * sin_B))

            if 0 <= o < 1760 and D > z_buffer[o]:
                z_buffer[o] = D
                frame_buffer[o] = ascii_chars[N if N > 0 else 0]

    # Move the cursor back to the top-left and print the frame in one go
    sys.stdout.write('\x1b[H' + ''.join(frame_buffer[k] + ('\n' if k % 80 == 79 else '') for k in range(1760)))
    sys.stdout.flush()

    # Increase the angles for the next frame (adjustable for smoothness)
    A += 0.07
    B += 0.03
