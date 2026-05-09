class MetodosOrdenamiento:

    def timSort(self, arreglo):
        arreglo.sort()
        print(arreglo)
        return arreglo

    def combSort(self, arreglo):
        gap = len(arreglo)
        shrink = 1.3
        sorteado = False
        while not sorteado:
            gap = int(gap // shrink)
            if gap <= 1:
                gap = 1
            sorteado = True
            for i in range(len(arreglo) - gap):
                if arreglo[i] > arreglo[i + gap]:
                    arreglo[i], arreglo[i + gap] = arreglo[i + gap], arreglo[i]
                    sorteado = False
        return arreglo

    def selectionSort(self, arreglo):
        for i in range(len(arreglo)):
            minIndex = i
            for j in range(i + 1, len(arreglo)):
                if arreglo[j] < arreglo[minIndex]:
                    minIndex = j
            arreglo[i], arreglo[minIndex] = arreglo[minIndex], arreglo[i]
        return arreglo

    def pigeonholeSort(self, arreglo):

        minValue = min(arreglo)
        maxValue = max(arreglo)
        size = maxValue - minValue + 1
        holes = [[] for _ in range(size)]

        for x in arreglo:
            holes[x - minValue].append(x)

        sortedArreglo = []
        for hole in holes:
            sortedArreglo.extend(hole)

        return sortedArreglo

    def bucketSort(self, arreglo):

        maxValue = max(arreglo)
        minValue = min(arreglo)
        rango = maxValue - minValue + 1
        numBuckets = len(arreglo) // 10 + 1
        buckets = [[] for _ in range(numBuckets)]

        for num in arreglo:
            index = (num - minValue) * numBuckets // rango
            buckets[index].append(num)

        for bucket in buckets:
            bucket.sort()

        sortedArreglo = []

        for bucket in buckets:
            sortedArreglo.extend(sorted(bucket))

        return sortedArreglo

    def quickSort(self, arreglo):
        if len(arreglo) <= 1:
            return arreglo
        pivot = arreglo[len(arreglo) // 2]
        left = [x for x in arreglo if x < pivot]
        mid = [x for x in arreglo if x == pivot]
        right = [x for x in arreglo if x > pivot]
        return self.quickSort(left) + mid + self.quickSort(right)

    def heapify(self, arreglo, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arreglo[i] < arreglo[left]:
            largest = left
        if right < n and arreglo[largest] < arreglo[right]:
            largest = right
        if largest != i:
            arreglo[i], arreglo[largest] = arreglo[largest], arreglo[i]
            self.heapify(arreglo, n, largest)

    def heapSort(self, arreglo):
        n = len(arreglo)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arreglo, n, i)
        for i in range(n - 1, 0, -1):
            arreglo[i], arreglo[0] = arreglo[0], arreglo[i]
            self.heapify(arreglo, i, 0)
        return arreglo

    def bitonicMerge(self, arreglo, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                if (direction == 1 and arreglo[i] > arreglo[i + k]) or (direction == 0 and arreglo[i] < arreglo[i + k]):
                    arreglo[i], arreglo[i + k] = arreglo[i + k], arreglo[i]
            self.bitonicMerge(arreglo, low, k, direction)
            self.bitonicMerge(arreglo, low + k, k, direction)

    def bitonicSortRecursive(self, arreglo, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            self.bitonicSortRecursive(arreglo, low, k, 1)
            self.bitonicSortRecursive(arreglo, low + k, k, 0)
            self.bitonicMerge(arreglo, low, cnt, direction)

    def bitonicSort(self, arreglo):
        self.bitonicSortRecursive(arreglo, 0, len(arreglo), 1)
        return arreglo

    def gnomeSort(self, arreglo):
        index = 0
        while index < len(arreglo):
            if index == 0 or arreglo[index] >= arreglo[index - 1]:
                index += 1
            else:
                arreglo[index], arreglo[index - 1] = arreglo[index - 1], arreglo[index]
                index -= 1
        return arreglo

    def binaryInsertionSort(self, arreglo):

        for i in range(1, len(arreglo)):
            clave = arreglo[i]
            izquierda, derecha = 0, i

            while izquierda < derecha:
                medio = (izquierda + derecha) // 2
                if arreglo[medio] < clave:
                    izquierda = medio + 1
                else:
                    derecha = medio

            arreglo = arreglo[:izquierda] + [clave] + arreglo[izquierda:i] + arreglo[i + 1:]

        return arreglo

    def radixSort(self, arreglo):
        if len(arreglo) == 0:
            return arreglo

        maxValue = max(arreglo)
        exp = 1

        while maxValue // exp > 0:
            arreglo = self.countingSort(arreglo, exp)
            exp *= 10
        return arreglo

    def countingSort(self, arreglo, exp):
        n = len(arreglo)
        output = [0] * n
        count = [0] * 10

        for i in arreglo:
            index = (i // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (arreglo[i] // exp) % 10
            output[count[index] - 1] = arreglo[i]
            count[index] -= 1

        return output

    @staticmethod
    def treeSort(arreglo):
        class Node:
            def __init__(self, key):
                self.value = key
                self.left = None
                self.right = None

        def insert(root, key):
            if root is None:
                return Node(key)
            elif key < root.value:
                root.left = insert(root.left, key)
            elif key > root.value:
                root.right = insert(root.right, key)
            return root

        def inorderTraversal(root, sortedArreglo):
            if root:
                inorderTraversal(root.left, sortedArreglo)
                sortedArreglo.append(root.value)
                inorderTraversal(root.right, sortedArreglo)

        root = None
        for key in arreglo:
            root = insert(root, key)

        sortedArreglo = []
        inorderTraversal(root, sortedArreglo)
        return sortedArreglo

    def bubbleSort(self, arreglo):
        n = len(arreglo)

        for i in range(n):
            swapped = False

            for j in range(0, n-i-1):
                if arreglo[j] > arreglo[j+1]:
                    arreglo[j], arreglo[j+1] = arreglo[j+1], arreglo[j]
                    swapped = True
            if (swapped == False):
                break