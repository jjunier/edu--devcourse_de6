from typing import Any
from doubly_linkedlist import Node, DoublyLinkedList


class PriorityQueue:
    def __init__(self):
        """
        양방향 연결 리스트(DoublyLinkedList)를 이용해 구현한 우선순위 큐를 초기화한다.

        이 구현은 '내림차순(큰 값이 앞)' 정렬 상태를 유지한다.
        - enqueue(x): 삽입 시 적절한 위치를 찾아 정렬 상태를 유지한다.
        - dequeue(): 가장 우선순위가 낮은 원소(가장 작은 값)를 제거하고 반환한다.
                    (내림차순 유지이므로 연결 리스트의 맨 뒤 원소)
        - peek(): dequeue 대상(맨 뒤 원소)을 제거하지 않고 반환한다.
        """
        self.queue = DoublyLinkedList()

    def size(self) -> int:
        """
        우선순위 큐에 들어있는 원소의 개수를 반환한다.

        Returns:
            int: 큐 원소 개수
        """
        return self.queue.getLength()

    def isEmpty(self) -> bool:
        """
        우선순위 큐가 비어있는지 여부를 반환한다.

        Returns:
            bool: 비어있으면 True, 아니면 False
        """
        return self.size() == 0

    def enqueue(self, x: Any) -> None:
        """
        원소 x를 우선순위 큐에 삽입한다.

        이 구현은 연결 리스트 내부를 '내림차순(큰 값이 앞)'으로 유지한다.
        따라서 삽입 시 다음 조건을 만족하는 위치를 찾는다.

        - curr를 head(더미)에서 시작했을 때,
          curr.next가 tail(더미)이 아니고 x < curr.next.data 인 동안 curr를 전진한다.
        - 반복 종료 후 curr 뒤에 x를 삽입하면,
          리스트는 내림차순 정렬을 유지한다.

        Args:
            x (Any): 삽입할 데이터 (비교 연산(<)이 가능해야 함)

        Returns:
            None
        """
        newNode = Node(x)
        curr = self.queue.head  # 더미 head에서 시작

        while True:
            assert curr.next is not None  # 더미 tail 구조상 None이면 구조가 깨짐
            if curr.next is self.queue.tail:
                break
            if not (x < curr.next.data):
                break
            curr = curr.next

        self.queue.insertAfter(curr, newNode)

    def dequeue(self) -> Any:
        """
        우선순위 큐에서 원소를 제거하고 반환한다.

        내림차순 정렬을 유지하므로,
        가장 작은 값(우선순위가 가장 낮은 값)은 리스트의 마지막 데이터 노드에 있다.
        따라서 마지막 위치(nodeCount)를 제거한다.

        Returns:
            Any: 제거된 원소

        Raises:
            IndexError: 큐가 비어있으면 발생
        """
        if self.isEmpty():
            raise IndexError("dequeue from empty priority queue")

        return self.queue.popAt(self.queue.getLength())

    def peek(self) -> Any:
        """
        dequeue 대상 원소(가장 작은 값)를 제거하지 않고 반환한다.

        Returns:
            Any: dequeue 대상 원소

        Raises:
            IndexError: 큐가 비어있으면 발생
        """
        if self.isEmpty():
            raise IndexError("peek from empty priority queue")

        node = self.queue.getAt(self.queue.getLength())
        if node is None:
            # 논리적으로는 여기 오면 내부 구조가 깨진 것
            raise RuntimeError("Linked list is corrupted: getAt returned None")

        return node.data
