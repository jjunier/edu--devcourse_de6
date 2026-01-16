from typing import Any
from doubly_linkedlist import Node, DoublyLinkedList


class ArrayQueue:
    def __init__(self):
        """
        파이썬 리스트(list)를 내부 저장소로 사용하는 큐를 초기화한다.

        - enqueue는 리스트의 끝에 추가한다.
        - dequeue는 리스트의 앞(0번 인덱스)에서 제거한다.
          (참고: list.pop(0)은 O(n)이므로 원소가 매우 많을 때는 비효율적일 수 있다.)
        """
        self.data = []

    def size(self) -> int:
        """
        큐에 들어있는 원소의 개수를 반환한다.

        Returns:
            int: 큐 원소 개수
        """
        return len(self.data)

    def isEmpty(self) -> bool:
        """
        큐가 비어있는지 여부를 반환한다.

        Returns:
            bool: 비어있으면 True, 아니면 False
        """
        return self.size() == 0

    def enqueue(self, item: Any) -> None:
        """
        큐의 뒤(rear)에 item을 추가한다.

        Args:
            item (Any): 큐에 넣을 데이터

        Returns:
            None
        """
        self.data.append(item)

    def dequeue(self) -> Any:
        """
        큐의 앞(front)에서 원소를 제거하고 반환한다.

        Returns:
            Any: 제거된 front 원소

        Raises:
            IndexError: 큐가 비어있으면 발생 (list.pop(0) 동작)
        """
        return self.data.pop(0)

    def peek(self) -> Any:
        """
        큐의 앞(front) 원소를 제거하지 않고 반환한다.

        Returns:
            Any: front 원소

        Raises:
            IndexError: 큐가 비어있으면 발생 (self.data[0] 접근)
        """
        return self.data[0]


class LinkedListQueue:
    def __init__(self):
        """
        양방향 연결 리스트(DoublyLinkedList)를 내부 저장소로 사용하는 큐를 초기화한다.

        - front는 연결 리스트의 1번 위치(첫 데이터 노드)에 해당한다.
        - rear는 연결 리스트의 마지막 위치(nodeCount)에 해당한다.
        - enqueue는 맨 뒤 삽입, dequeue는 맨 앞 삭제로 구현한다.
        """
        self.data = DoublyLinkedList()

    def size(self) -> int:
        """
        큐에 들어있는 원소의 개수를 반환한다.

        내부적으로는 연결 리스트의 길이(nodeCount)를 반환한다.

        Returns:
            int: 큐 원소 개수
        """
        return self.data.getLength()

    def isEmpty(self) -> bool:
        """
        큐가 비어있는지 여부를 반환한다.

        Returns:
            bool: 비어있으면 True, 아니면 False
        """
        return self.size() == 0

    def enqueue(self, item: Any) -> None:
        """
        큐의 뒤(rear)에 item을 추가한다.

        양방향 연결 리스트의 마지막 위치(nodeCount + 1)에 삽입한다.

        Args:
            item (Any): 큐에 넣을 데이터

        Returns:
            None
        """
        node = Node(item)
        self.data.insertAt(self.size() + 1, node)

    def dequeue(self) -> Any:
        """
        큐의 앞(front)에서 원소를 제거하고 반환한다.

        양방향 연결 리스트의 1번 위치(첫 데이터 노드)를 삭제한다.

        Returns:
            Any: 제거된 front 원소

        Raises:
            IndexError: 큐가 비어있으면 발생 (popAt이 예외 발생)
        """
        return self.data.popAt(1)

    def peek(self) -> Any:
        """
        큐의 앞(front) 원소를 제거하지 않고 반환한다.

        Returns:
            Any: front 원소

        Raises:
            IndexError: 큐가 비어있으면 발생 (빈 큐에서 front 조회 불가)
        """
        if self.isEmpty():
            raise IndexError("peek from empty queue")

        node = self.data.getAt(1)
        if node is None:
            # 논리적으로는 여기 오면 내부 구조가 깨진 것
            raise RuntimeError("Linked list is corrupted: getAt returned None")

        return node.data
