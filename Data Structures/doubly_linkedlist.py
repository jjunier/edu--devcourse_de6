from typing import Any, Optional, List


class Node:
    def __init__(self, item: Any):
        """
        양방향 연결 리스트를 구성하는 노드를 초기화한다.

        Args:
            item (Any): 노드에 저장할 데이터
        """
        self.data = item
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class DoublyLinkedList:
    def __init__(self):
        """
        더미(dummy) head/tail 노드를 사용하는 양방향 연결 리스트를 초기화한다.

        - 실제 데이터 노드들은 head와 tail 사이(head.next ~ tail.prev)에 존재한다.
        - 빈 리스트일 때:
            nodeCount == 0
            head.next == tail
            tail.prev == head
        - head.prev는 항상 None, tail.next는 항상 None이다.
        """
        self.nodeCount = 0
        self.head = Node(None)
        self.tail = Node(None)

        self.head.prev = None
        self.head.next = self.tail
        self.tail.prev = self.head
        self.tail.next = None

    def traverse(self) -> List[Any]:
        """
        리스트의 앞(head 방향)에서 뒤(tail 방향)로 순회하며
        저장된 모든 데이터를 리스트로 반환한다.

        더미 노드(head, tail)는 결과에 포함하지 않는다.

        Returns:
            list: 연결 리스트에 저장된 데이터들의 리스트
        """
        result: List[Any] = []
        curr = self.head.next

        while curr is not None and curr is not self.tail:
            result.append(curr.data)
            curr = curr.next

        return result

    def reverse(self) -> List[Any]:
        """
        리스트의 뒤(tail 방향)에서 앞(head 방향)로 역순회하며
        저장된 모든 데이터를 리스트로 반환한다.

        더미 노드(head, tail)는 결과에 포함하지 않는다.

        Returns:
            list: 연결 리스트에 저장된 데이터들의 리스트(역순)
        """
        result: List[Any] = []
        curr = self.tail.prev

        while curr is not None and curr is not self.head:
            result.append(curr.data)
            curr = curr.prev

        return result

    def getAt(self, pos: int) -> Optional[Node]:
        """
        지정한 위치(pos)의 노드를 반환한다.

        더미 head를 0번 인덱스로 취급한다.
        - pos == 0              : head(더미) 반환
        - pos == 1              : 첫 데이터 노드 반환
        - pos == nodeCount      : 마지막 데이터 노드 반환
        - pos == nodeCount + 1  : tail(더미) 반환

        내부적으로 pos가 리스트의 앞/뒤 중 어디에 가까운지에 따라
        head 또는 tail에서 시작하여 탐색 시간을 줄인다.

        Args:
            pos (int): 가져올 노드의 위치 (0 이상 nodeCount + 1 이하)

        Returns:
            Node or None: 해당 위치의 노드, 범위를 벗어나면 None
        """
        if pos < 0 or pos > self.nodeCount + 1:
            return None

        # tail까지 포함해 접근 가능하도록 범위를 nodeCount+1로 둔다.
        # (예: insertAfter(tail.prev, ...) / insertBefore(tail, ...) 같은 조합을 위해)
        if pos > (self.nodeCount + 1) // 2:
            # tail에서 뒤로 이동: tail이 (nodeCount+1) 위치
            i = 0
            curr = self.tail
            steps = (self.nodeCount + 1) - pos
            while i < steps and curr is not None:
                curr = curr.prev
                i += 1
        else:
            # head에서 앞으로 이동: head가 0 위치
            i = 0
            curr = self.head
            while i < pos and curr is not None:
                curr = curr.next
                i += 1

        return curr

    def insertAfter(self, prev: Node, newNode: Node) -> bool:
        """
        주어진 노드 prev의 뒤에 newNode를 삽입한다.

        더미 tail을 사용하므로, prev가 tail인 경우는 허용하지 않는다.
        (tail 뒤에는 실제 노드가 올 수 없기 때문)

        Args:
            prev (Node): 삽입 기준이 되는 이전 노드
            newNode (Node): 새로 삽입할 노드

        Returns:
            bool: 삽입 성공 여부
        """
        if prev is None or prev is self.tail:
            return False

        nxt = prev.next
        if nxt is None:
            # 더미 tail 구조에서 prev.next가 None이면 구조가 깨진 것
            return False

        newNode.prev = prev
        newNode.next = nxt
        prev.next = newNode
        nxt.prev = newNode

        self.nodeCount += 1
        return True

    def insertBefore(self, nxt: Node, newNode: Node) -> bool:
        """
        주어진 노드 nxt의 앞에 newNode를 삽입한다.

        더미 head를 사용하므로, nxt가 head인 경우는 허용하지 않는다.
        (head 앞에는 실제 노드가 올 수 없기 때문)

        Args:
            nxt (Node): 삽입 기준이 되는 다음 노드
            newNode (Node): 새로 삽입할 노드

        Returns:
            bool: 삽입 성공 여부
        """
        if nxt is None or nxt is self.head:
            return False

        prev = nxt.prev
        if prev is None:
            # 더미 head 구조에서 nxt.prev가 None이면 구조가 깨진 것
            return False

        newNode.prev = prev
        newNode.next = nxt
        prev.next = newNode
        nxt.prev = newNode

        self.nodeCount += 1
        return True

    def insertAt(self, pos: int, newNode: Node) -> bool:
        """
        지정한 위치(pos)에 newNode를 삽입한다.

        pos는 실제 데이터 노드 기준으로 1부터 시작한다.
        - pos == 1              : 맨 앞(첫 데이터 노드 자리)에 삽입
        - pos == nodeCount + 1  : 맨 뒤(마지막 뒤)에 삽입

        구현은 다음 2단계로 수행한다.
        1) pos-1 위치(이전 노드)를 getAt으로 찾는다. (더미 head 포함)
        2) insertAfter(prev, newNode)로 실제 삽입(링크 조작)을 수행한다.

        Args:
            pos (int): 삽입할 위치 (1 이상 nodeCount + 1 이하)
            newNode (Node): 새로 삽입할 노드

        Returns:
            bool: 삽입 성공 여부
        """
        if pos < 1 or pos > self.nodeCount + 1:
            return False

        prev = self.getAt(pos - 1)
        if prev is None:
            return False

        return self.insertAfter(prev, newNode)

    def popAfter(self, prev: Node) -> Optional[Any]:
        """
        주어진 노드 prev의 '다음 노드'를 제거하고 데이터를 반환한다.

        다음 노드가 더미 tail이면 삭제할 실제 노드가 없으므로 None을 반환한다.

        Args:
            prev (Node): 삭제 대상 노드의 이전 노드

        Returns:
            Any or None: 제거된 노드의 데이터, 삭제할 노드가 없으면 None
        """
        if prev is None or prev is self.tail:
            return None

        curr = prev.next
        if curr is None or curr is self.tail:
            return None

        nxt = curr.next
        if nxt is None:
            # 더미 tail 구조에서 curr.next가 None이면 구조가 깨진 것
            return None

        prev.next = nxt
        nxt.prev = prev

        self.nodeCount -= 1

        # 안전하게 분리(선택 사항)
        curr.prev = None
        curr.next = None

        return curr.data

    def popBefore(self, nxt: Node) -> Optional[Any]:
        """
        주어진 노드 nxt의 '이전 노드'를 제거하고 데이터를 반환한다.

        이전 노드가 더미 head이면 삭제할 실제 노드가 없으므로 None을 반환한다.

        Args:
            nxt (Node): 삭제 대상 노드의 다음 노드

        Returns:
            Any or None: 제거된 노드의 데이터, 삭제할 노드가 없으면 None
        """
        if nxt is None or nxt is self.head:
            return None

        curr = nxt.prev
        if curr is None or curr is self.head:
            return None

        prev = curr.prev
        if prev is None:
            # 더미 head 구조에서 curr.prev가 None이면 구조가 깨진 것
            return None

        prev.next = nxt
        nxt.prev = prev

        self.nodeCount -= 1

        # 안전하게 분리(선택 사항)
        curr.prev = None
        curr.next = None

        return curr.data

    def popAt(self, pos: int) -> Any:
        """
        지정한 위치(pos)의 노드를 제거하고 해당 데이터를 반환한다.

        pos는 실제 데이터 노드 기준으로 1부터 시작한다.

        Args:
            pos (int): 제거할 노드의 위치 (1부터 시작)

        Returns:
            Any: 제거된 노드의 데이터

        Raises:
            IndexError: pos가 유효 범위를 벗어나면 발생
        """
        if pos < 1 or pos > self.nodeCount:
            raise IndexError("pos out of range")

        prev = self.getAt(pos - 1)
        if prev is None:
            raise IndexError("pos out of range")

        data = self.popAfter(prev)
        if data is None:
            # 범위 검증을 했으므로 보통 발생하지 않지만, 방어적으로 처리
            raise IndexError("pos out of range")

        return data

    def concat(self, L: "DoublyLinkedList") -> None:
        """
        현재 리스트 뒤에 또 다른 리스트 L을 이어 붙인다.

        - L이 빈 리스트면 아무 변화가 없다.
        - 이어 붙인 뒤 현재 리스트는 노드 수가 증가하고,
          L은 빈 리스트 상태(head<->tail만 남는 상태)로 만든다.
        - 더미 head/tail을 사용하는 구조이므로,
          실제 연결은 self.tail.prev와 L.head.next 사이를 잇는 방식으로 수행한다.

        Args:
            L (DoublyLinkedList): 현재 리스트 뒤에 이어 붙일 리스트

        Returns:
            None
        """
        if L.nodeCount == 0:
            return

        # self의 마지막 데이터 노드, L의 첫/마지막 데이터 노드
        last_self = self.tail.prev
        first_L = L.head.next
        last_L = L.tail.prev

        # 방어적 체크(구조가 깨진 경우 대비)
        if last_self is None or first_L is None or last_L is None:
            return
        if last_self is self.head:  # self가 비어있다면 last_self==head
            # self가 비어있는 경우: head와 tail 사이에 L의 데이터를 그대로 끼워넣기
            self.head.next = first_L
            first_L.prev = self.head
            last_L.next = self.tail
            self.tail.prev = last_L
        else:
            # 일반 케이스: self의 마지막과 L의 첫 노드를 연결
            last_self.next = first_L
            first_L.prev = last_self
            last_L.next = self.tail
            self.tail.prev = last_L

        self.nodeCount += L.nodeCount

        # L을 빈 리스트로 초기화 (더미끼리만 연결되도록 복구)
        L.head.next = L.tail
        L.tail.prev = L.head
        L.nodeCount = 0

    def getLength(self) -> int:
        """
        연결 리스트에 저장된 실제 데이터 노드의 개수(nodeCount)를 반환한다.

        스택/큐 등 다른 자료구조 구현에서 길이가 필요할 때,
        내부 표현(더미 head/tail)을 노출하지 않고 O(1)로 길이를 제공하기 위해 사용된다.

        Returns:
            int: 연결 리스트의 길이(실제 데이터 노드의 개수)
        """
        return self.nodeCount
