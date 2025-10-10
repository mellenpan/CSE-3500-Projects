import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):
        energy_values = {} #stores energy values

        def get_energy(x, y):
            if (x,y) not in energy_values:
                energy_values[(x,y)] = self.energy(x,y)
            return energy_values[(x,y)]


        if dp:
            width = self.width
            height = self.height

            cost = [[0]* width for h in range(height)] #records least energy 
            path = [[0]* width for h in range(height)] #stores which x-position in the row above has min energy path

            for x in range(width):
                cost[0][x] = get_energy(x, 0)

            for y in range(1, height):
                for x in range(width):
                    smallest_prev = cost[y-1][x]
                    best_x = x
                    if x > 0 and cost[y-1][x-1] < smallest_prev: #if x is greater than 0 and cost of x to the TOP-LEFT is less than smallest_prev
                        smallest_prev = cost[y-1][x-1]
                        best_x = x-1
                    if x < width -1 and cost[y-1][x+1] < smallest_prev: #if x to the TOP-RIGHT is larger than the smallest_prev stored
                        smallest_prev = cost[y-1][x+1]
                        best_x = x+1
                    cost[y][x] = get_energy(x,y) + smallest_prev
                    path[y][x] = best_x

            final_min_x = min(range(width), key = lambda x: cost[height-1][x])
            seam = []
            x = final_min_x

            for y in reversed(range(height)):
                seam.append((x,y))
                x = path[y][x]
            return seam[::-1]
        
        else:   #if DP is false
            def compute_cost(x, y):
                if x < 0 or x >= self.width:
                    return float('inf')
                if y == 0:
                    return get_energy(x, 0)
                return get_energy(x, y) + min(
                    compute_cost(x - 1, y - 1),
                    compute_cost(x, y - 1),
                    compute_cost(x + 1, y - 1))
            min_total = float('inf')
            min_end_x = 0
            for x in range(self.width):
                total = compute_cost(x, self.height - 1)
                if total < min_total:
                    min_total = total
                    min_end_x = x

            # Reconstruct path
            seam = []
            x = min_end_x
            for y in reversed(range(self.height)):
                seam.append((x, y))
                # Choose previous pixel (min of 3 directions)
                options = [(x2, compute_cost(x2, y - 1)) for x2 in [x - 1, x, x + 1] if 0 <= x2 < self.width]
                if y > 0 and options:
                    x = min(options, key=lambda item: item[1])[0]
            return seam[::-1]
