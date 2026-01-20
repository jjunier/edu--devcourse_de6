from typing import Any, Optional

class MaxHeap:
    def __init__(self) -> None:
        self.data: list[Any] = [None]

    def insert(self, item: Any) -> None:
        """
        힙에 새로운 원소를 삽입한다.
        
        Args:
            item (Any): 힙에 삽입할 데이터
        """
        self.data.append(item)
        i: int = len(self.data) - 1

        while i > 1:
            parent = i // 2

            if self.data[parent] < self.data[i]:
                self.data[parent], self.data[i] = self.data[i], self.data[parent]
                i = parent
            
            else:
                break

    def remove(self) -> Optional[Any]:
        """
        최대 힙에서 최댓값을 제거하고 반환한다.

        Returns:
            Optional[Any]: 제거된 최댓값, 
                            만약 힙이 비어있다면 None
        """
        if len(self.data) > 1:
            self.data[1], self.data[-1] = self.data[-1], self.data[1]
            data = self.data.pop(-1)
            self.maxHeapify(1)
        else:
            data = None
        
        return data
    
    def maxHeapify(self, i: int) -> None:
        """
        인덱스 i를 기준으로 최대 힙 성질을 복구한다.

        Args:
            i (int): 힙 성질을 복구할 시작 인덱스
        """
        left: int = 2 * i
        right: int = 2 * i + 1
        smallest: int = i

        if left < len(self.data) and self.data[left] > self.data[smallest]:
            smallest = left
        
        if right < len(self.data) and self.data[right] > self.data[smallest]:
            smallest = right

        if smallest != i:
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            self.maxHeapify(smallest)
