from typing import Any, List, Optional


class CircularQueue:
    def __init__(self, n: int):
        """
        배열 기반 환형 큐(Circular Queue)를 초기화한다.

        이 구현은 'count(현재 원소 수)'를 별도로 유지하여,
        front/rear 포인터가 같아지는 상황에서도 빈/가득 참을 구분한다.

        - maxCount: 큐의 최대 용량(배열 크기)
        - data: 실제 데이터를 저장하는 배열
        - count: 현재 큐에 들어있는 원소 개수
        - front: 마지막으로 dequeue된 위치(초기 -1)
        - rear:  마지막으로 enqueue된 위치(초기 -1)

        빈 큐에서 다음 dequeue가 일어날 실제 front 원소의 인덱스는
        (front + 1) % maxCount 로 계산된다.

        Args:
            n (int): 큐의 최대 용량 (1 이상이어야 함)

        Raises:
            ValueError: n이 1 미만이면 발생
        """
        if n < 1:
            raise ValueError("Queue capacity must be at least 1")

        self.maxCount: int = n
        self.data: List[Optional[Any]] = [None] * n
        self.count: int = 0
        self.front: int = -1
        self.rear: int = -1

    def size(self) -> int:
        """
        큐에 들어있는 원소의 개수를 반환한다.

        Returns:
            int: 큐 원소 개수
        """
        return self.count

    def isEmpty(self) -> bool:
        """
        큐가 비어있는지 여부를 반환한다.

        Returns:
            bool: 비어있으면 True, 아니면 False
        """
        return self.count == 0

    def isFull(self) -> bool:
        """
        큐가 가득 찼는지 여부를 반환한다.

        Returns:
            bool: 가득 찼으면 True, 아니면 False
        """
        return self.count == self.maxCount

    def enqueue(self, x: Any) -> None:
        """
        큐의 뒤(rear)에 원소 x를 추가한다.

        rear 포인터를 한 칸 전진시키되, 배열의 끝을 넘어가면
        처음(0)으로 되돌아오도록 모듈러 연산을 사용한다.

        Args:
            x (Any): 큐에 넣을 데이터

        Returns:
            None

        Raises:
            IndexError: 큐가 가득 찼으면 발생
        """
        if self.isFull():
            raise IndexError("Queue Full")

        self.rear = (self.rear + 1) % self.maxCount
        self.data[self.rear] = x
        self.count += 1

    def dequeue(self) -> Any:
        """
        큐의 앞(front)에서 원소를 제거하고 반환한다.

        front 포인터를 한 칸 전진시키되, 배열의 끝을 넘어가면
        처음(0)으로 되돌아오도록 모듈러 연산을 사용한다.

        Returns:
            Any: 제거된 front 원소

        Raises:
            IndexError: 큐가 비어있으면 발생
        """
        if self.isEmpty():
            raise IndexError("Queue Empty")

        self.front = (self.front + 1) % self.maxCount
        x = self.data[self.front]

        # 선택 사항: 디버깅/메모리 참조를 위해 제거한 자리를 None 처리
        self.data[self.front] = None

        self.count -= 1
        return x

    def peek(self) -> Any:
        """
        큐의 앞(front) 원소를 제거하지 않고 반환한다.

        실제 front 원소의 인덱스는 (front + 1) % maxCount 로 계산된다.

        Returns:
            Any: front 원소

        Raises:
            IndexError: 큐가 비어있으면 발생
        """
        if self.isEmpty():
            raise IndexError("Queue Empty")

        return self.data[(self.front + 1) % self.maxCount]
